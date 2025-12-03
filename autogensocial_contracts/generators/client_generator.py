"""
Client code generator from OpenAPI specifications.

This module provides utilities to generate API client code from OpenAPI 3.0
specifications for various programming languages.
"""

from typing import Any, Dict, List, Optional
from pathlib import Path
import yaml


class ClientGenerator:
    """Generate API client code from OpenAPI specifications."""
    
    def __init__(self, openapi_path: Optional[Path] = None):
        """
        Initialize client generator.
        
        Args:
            openapi_path: Optional path to OpenAPI directory. If not provided,
                         uses the package's openapi directory.
        """
        self.openapi_path = openapi_path
        if self.openapi_path is None:
            from autogensocial_contracts import openapi
            self.openapi_path = Path(openapi.__file__).parent
    
    def load_spec(self, spec_name: str) -> Dict[str, Any]:
        """
        Load an OpenAPI specification by name.
        
        Args:
            spec_name: Name of the spec (e.g., 'content-api', 'publisher')
            
        Returns:
            Dictionary containing the OpenAPI specification
        """
        spec_file = self.openapi_path / f"{spec_name}.yaml"
        with open(spec_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def get_endpoints(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract endpoints from OpenAPI spec.
        
        Args:
            spec: OpenAPI specification dictionary
            
        Returns:
            Dictionary of paths and their operations
        """
        return spec.get('paths', {})
    
    def get_base_url(self, spec: Dict[str, Any]) -> str:
        """
        Get base URL from OpenAPI spec.
        
        Args:
            spec: OpenAPI specification dictionary
            
        Returns:
            Base URL string
        """
        servers = spec.get('servers', [])
        if servers:
            return servers[0].get('url', '')
        return ''
    
    def generate_client(
        self,
        spec_name: str,
        output_format: str = "python",
        class_name: Optional[str] = None
    ) -> str:
        """
        Generate API client code.
        
        Args:
            spec_name: Name of the OpenAPI spec
            output_format: Output format ('python', 'typescript')
            class_name: Optional custom class name for the client
            
        Returns:
            Generated client code as string
        """
        spec = self.load_spec(spec_name)
        
        if class_name is None:
            class_name = spec.get('info', {}).get('title', 'API').replace(' ', '') + 'Client'
        
        if output_format == "python":
            return self._generate_python_client(spec, class_name)
        elif output_format == "typescript":
            return self._generate_typescript_client(spec, class_name)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    def _generate_python_client(self, spec: Dict[str, Any], class_name: str) -> str:
        """Generate Python API client."""
        base_url = self.get_base_url(spec)
        endpoints = self.get_endpoints(spec)
        
        methods = []
        for path, path_item in endpoints.items():
            for method, operation in path_item.items():
                if method.lower() not in ['get', 'post', 'put', 'patch', 'delete']:
                    continue
                
                method_code = self._generate_python_method(
                    path, method.lower(), operation
                )
                methods.append(method_code)
        
        methods_str = "\n\n    ".join(methods)
        
        return f'''"""
Auto-generated API client from OpenAPI specification.
"""

from typing import Any, Dict, List, Optional
import httpx


class {class_name}:
    """API client for {spec.get('info', {}).get('title', 'API')}."""
    
    def __init__(
        self,
        base_url: str = "{base_url}",
        api_key: Optional[str] = None,
        timeout: float = 30.0
    ):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL for the API
            api_key: Optional API key for authentication
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for requests."""
        headers = {{"Content-Type": "application/json"}}
        if self.api_key:
            headers["Authorization"] = f"Bearer {{self.api_key}}"
        return headers
    
    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
    
    {methods_str}
'''
    
    def _generate_python_method(
        self,
        path: str,
        method: str,
        operation: Dict[str, Any]
    ) -> str:
        """Generate a Python method for an API operation."""
        operation_id = operation.get('operationId', f"{method}_{path.replace('/', '_')}")
        summary = operation.get('summary', 'API operation')
        
        # Extract path parameters
        path_params = []
        query_params = []
        has_body = False
        
        parameters = operation.get('parameters', [])
        for param in parameters:
            param_name = param.get('name', 'param')
            param_in = param.get('in', 'query')
            
            if param_in == 'path':
                path_params.append(param_name)
            elif param_in == 'query':
                query_params.append(param_name)
        
        if method in ['post', 'put', 'patch']:
            has_body = operation.get('requestBody') is not None
        
        # Build method signature
        params = []
        if path_params:
            params.extend([f"{p}: str" for p in path_params])
        if has_body:
            params.append("data: Dict[str, Any]")
        if query_params:
            params.extend([f"{p}: Optional[str] = None" for p in query_params])
        
        params_str = ", ".join(params) if params else ""
        
        # Build URL construction
        url_path = path
        for param in path_params:
            url_path = url_path.replace(f"{{{param}}}", f"{{{{param}}}}")
        
        # Build query params
        query_str = ""
        if query_params:
            query_parts = [f'"{p}": {p}' for p in query_params]
            query_str = f"""
        params = {{{", ".join(query_parts)}}}
        params = {{k: v for k, v in params.items() if v is not None}}"""
        
        # Build request call
        if method == 'get':
            request_call = f'''
        response = await self.client.get(
            url,
            headers=self._get_headers(){",\n            params=params" if query_params else ""}
        )'''
        elif method in ['post', 'put', 'patch']:
            request_call = f'''
        response = await self.client.{method}(
            url,
            headers=self._get_headers(),
            json=data{",\n            params=params" if query_params else ""}
        )'''
        else:  # delete
            request_call = f'''
        response = await self.client.delete(
            url,
            headers=self._get_headers(){",\n            params=params" if query_params else ""}
        )'''
        
        return f'''async def {operation_id}(
        self{", " + params_str if params_str else ""}
    ) -> Any:
        """
        {summary}
        """
        url = f"{{self.base_url}}{url_path}"{query_str}{request_call}
        response.raise_for_status()
        return response.json() if response.content else None'''
    
    def _generate_typescript_client(self, spec: Dict[str, Any], class_name: str) -> str:
        """Generate TypeScript API client."""
        base_url = self.get_base_url(spec)
        endpoints = self.get_endpoints(spec)
        
        methods = []
        for path, path_item in endpoints.items():
            for method, operation in path_item.items():
                if method.lower() not in ['get', 'post', 'put', 'patch', 'delete']:
                    continue
                
                method_code = self._generate_typescript_method(
                    path, method.lower(), operation
                )
                methods.append(method_code)
        
        methods_str = "\n\n  ".join(methods)
        
        return f'''/**
 * Auto-generated API client from OpenAPI specification.
 */

export interface {class_name}Config {{
  baseUrl?: string;
  apiKey?: string;
  timeout?: number;
}}

export class {class_name} {{
  private baseUrl: string;
  private apiKey?: string;
  private timeout: number;

  constructor(config: {class_name}Config = {{}}) {{
    this.baseUrl = (config.baseUrl || '{base_url}').replace(/\\/+$/, '');
    this.apiKey = config.apiKey;
    this.timeout = config.timeout || 30000;
  }}

  private getHeaders(): HeadersInit {{
    const headers: HeadersInit = {{
      'Content-Type': 'application/json',
    }};
    
    if (this.apiKey) {{
      headers['Authorization'] = `Bearer ${{this.apiKey}}`;
    }}
    
    return headers;
  }}

  {methods_str}
}}
'''
    
    def _generate_typescript_method(
        self,
        path: str,
        method: str,
        operation: Dict[str, Any]
    ) -> str:
        """Generate a TypeScript method for an API operation."""
        operation_id = operation.get('operationId', f"{method}_{path.replace('/', '_')}")
        summary = operation.get('summary', 'API operation')
        
        # Extract path parameters
        path_params = []
        query_params = []
        has_body = False
        
        parameters = operation.get('parameters', [])
        for param in parameters:
            param_name = param.get('name', 'param')
            param_in = param.get('in', 'query')
            
            if param_in == 'path':
                path_params.append(param_name)
            elif param_in == 'query':
                query_params.append(param_name)
        
        if method in ['post', 'put', 'patch']:
            has_body = operation.get('requestBody') is not None
        
        # Build method signature
        params = []
        if path_params:
            params.extend([f"{p}: string" for p in path_params])
        if has_body:
            params.append("data: any")
        if query_params:
            params.extend([f"{p}?: string" for p in query_params])
        
        params_str = params[0] if len(params) == 1 else (
            f"{{\n    {',\n    '.join(params)}\n  }}: {{\n    {'; '.join(params)};\n  }}"
            if len(params) > 1 else ""
        )
        
        # Build URL
        url_path = path
        for param in path_params:
            url_path = url_path.replace(f"{{{param}}}", f"${{{param}}}")
        
        # Build query params
        query_str = ""
        if query_params:
            query_parts = [f'if ({p}) params.append("{p}=" + {p})' for p in query_params]
            query_str = f"""
    const params: string[] = [];
    {'; '.join(query_parts)};
    const queryString = params.length > 0 ? '?' + params.join('&') : '';"""
        
        # Build fetch options
        fetch_options = "method, headers: this.getHeaders()"
        if has_body:
            fetch_options += ", body: JSON.stringify(data)"
        
        return f'''async {operation_id}({params_str}): Promise<any> {{
    /**
     * {summary}
     */{query_str}
    const url = `${{this.baseUrl}}{url_path}${{queryString || ''}}`;
    
    const response = await fetch(url, {{
      method: '{method.upper()}',
      headers: this.getHeaders(),{' body: JSON.stringify(data),' if has_body else ''}
    }});
    
    if (!response.ok) {{
      throw new Error(`API error: ${{response.statusText}}`);
    }}
    
    return response.json();
  }}'''
