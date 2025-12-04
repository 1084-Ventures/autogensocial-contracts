"""
CRUD operation generator from JSON schemas.

This module provides utilities to generate Create, Read, Update, Delete (CRUD)
operations and database models from JSON schema definitions.
"""

from typing import Any, Dict, List, Optional
from pathlib import Path
import json


class CRUDGenerator:
    """Generate CRUD operations from JSON schemas."""
    
    def __init__(self, schema_path: Optional[Path] = None):
        """
        Initialize CRUD generator.
        
        Args:
            schema_path: Optional path to schema directory. If not provided,
                        uses the package's schema directory.
        """
        self.schema_path = schema_path
        if self.schema_path is None:
            from autogensocial_contracts import schemas
            self.schema_path = Path(schemas.__file__).parent
    
    def load_schema(self, schema_name: str) -> Dict[str, Any]:
        """
        Load a JSON schema by name.
        
        Args:
            schema_name: Name of the schema (e.g., 'brand', 'post')
            
        Returns:
            Dictionary containing the JSON schema
        """
        schema_file = self.schema_path / f"{schema_name}.json"
        with open(schema_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_model_name(self, schema: Dict[str, Any]) -> str:
        """
        Extract model name from schema.
        
        Args:
            schema: JSON schema dictionary
            
        Returns:
            Model name (e.g., 'Brand', 'Post')
        """
        return schema.get('title', 'UnknownModel')
    
    def get_required_fields(self, schema: Dict[str, Any]) -> List[str]:
        """
        Get list of required fields from schema.
        
        Args:
            schema: JSON schema dictionary
            
        Returns:
            List of required field names
        """
        return schema.get('required', [])
    
    def get_properties(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get properties from schema.
        
        Args:
            schema: JSON schema dictionary
            
        Returns:
            Dictionary of property definitions
        """
        return schema.get('properties', {})
    
    def generate_create_operation(
        self, 
        schema_name: str,
        output_format: str = "python"
    ) -> str:
        """
        Generate CREATE operation code.
        
        Args:
            schema_name: Name of the schema
            output_format: Output format ('python', 'typescript', 'sql')
            
        Returns:
            Generated code as string
        """
        schema = self.load_schema(schema_name)
        model_name = self.get_model_name(schema)
        
        if output_format == "python":
            return self._generate_python_create(model_name, schema)
        elif output_format == "typescript":
            return self._generate_typescript_create(model_name, schema)
        elif output_format == "sql":
            return self._generate_sql_create(model_name, schema)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    def generate_read_operation(
        self,
        schema_name: str,
        output_format: str = "python"
    ) -> str:
        """
        Generate READ operation code.
        
        Args:
            schema_name: Name of the schema
            output_format: Output format ('python', 'typescript', 'sql')
            
        Returns:
            Generated code as string
        """
        schema = self.load_schema(schema_name)
        model_name = self.get_model_name(schema)
        
        if output_format == "python":
            return self._generate_python_read(model_name, schema)
        elif output_format == "typescript":
            return self._generate_typescript_read(model_name, schema)
        elif output_format == "sql":
            return self._generate_sql_read(model_name, schema)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    def generate_update_operation(
        self,
        schema_name: str,
        output_format: str = "python"
    ) -> str:
        """
        Generate UPDATE operation code.
        
        Args:
            schema_name: Name of the schema
            output_format: Output format ('python', 'typescript', 'sql')
            
        Returns:
            Generated code as string
        """
        schema = self.load_schema(schema_name)
        model_name = self.get_model_name(schema)
        
        if output_format == "python":
            return self._generate_python_update(model_name, schema)
        elif output_format == "typescript":
            return self._generate_typescript_update(model_name, schema)
        elif output_format == "sql":
            return self._generate_sql_update(model_name, schema)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    def generate_delete_operation(
        self,
        schema_name: str,
        output_format: str = "python"
    ) -> str:
        """
        Generate DELETE operation code.
        
        Args:
            schema_name: Name of the schema
            output_format: Output format ('python', 'typescript', 'sql')
            
        Returns:
            Generated code as string
        """
        schema = self.load_schema(schema_name)
        model_name = self.get_model_name(schema)
        
        if output_format == "python":
            return self._generate_python_delete(model_name, schema)
        elif output_format == "typescript":
            return self._generate_typescript_delete(model_name, schema)
        elif output_format == "sql":
            return self._generate_sql_delete(model_name, schema)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    def generate_all_operations(
        self,
        schema_name: str,
        output_format: str = "python"
    ) -> Dict[str, str]:
        """
        Generate all CRUD operations for a schema.
        
        Args:
            schema_name: Name of the schema
            output_format: Output format ('python', 'typescript', 'sql')
            
        Returns:
            Dictionary with keys 'create', 'read', 'update', 'delete'
        """
        return {
            'create': self.generate_create_operation(schema_name, output_format),
            'read': self.generate_read_operation(schema_name, output_format),
            'update': self.generate_update_operation(schema_name, output_format),
            'delete': self.generate_delete_operation(schema_name, output_format),
        }
    
    # Private helper methods for Python code generation
    def _generate_python_create(self, model_name: str, schema: Dict[str, Any]) -> str:
        """Generate Python CREATE operation."""
        return f"""async def create_{model_name.lower()}(
    {model_name.lower()}: {model_name},
    db: AsyncSession
) -> {model_name}:
    '''
    Create a new {model_name}.
    
    Args:
        {model_name.lower()}: {model_name} data to create
        db: Database session
        
    Returns:
        Created {model_name} instance
    '''
    db_{model_name.lower()} = {model_name}DB(**{model_name.lower()}.model_dump())
    db.add(db_{model_name.lower()})
    await db.commit()
    await db.refresh(db_{model_name.lower()})
    return {model_name}.model_validate(db_{model_name.lower()})
"""
    
    def _generate_python_read(self, model_name: str, schema: Dict[str, Any]) -> str:
        """Generate Python READ operation."""
        return f"""async def get_{model_name.lower()}(
    {model_name.lower()}_id: str,
    db: AsyncSession
) -> Optional[{model_name}]:
    '''
    Get a {model_name} by ID.
    
    Args:
        {model_name.lower()}_id: ID of the {model_name} to retrieve
        db: Database session
        
    Returns:
        {model_name} instance if found, None otherwise
    '''
    result = await db.execute(
        select({model_name}DB).where({model_name}DB.id == {model_name.lower()}_id)
    )
    db_{model_name.lower()} = result.scalar_one_or_none()
    if db_{model_name.lower()}:
        return {model_name}.model_validate(db_{model_name.lower()})
    return None

async def list_{model_name.lower()}s(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> List[{model_name}]:
    '''
    List all {model_name}s.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of {model_name} instances
    '''
    result = await db.execute(
        select({model_name}DB).offset(skip).limit(limit)
    )
    db_{model_name.lower()}s = result.scalars().all()
    return [{model_name}.model_validate(item) for item in db_{model_name.lower()}s]
"""
    
    def _generate_python_update(self, model_name: str, schema: Dict[str, Any]) -> str:
        """Generate Python UPDATE operation."""
        return f"""async def update_{model_name.lower()}(
    {model_name.lower()}_id: str,
    {model_name.lower()}_update: {model_name}Update,
    db: AsyncSession
) -> Optional[{model_name}]:
    '''
    Update a {model_name}.
    
    Args:
        {model_name.lower()}_id: ID of the {model_name} to update
        {model_name.lower()}_update: Updated {model_name} data
        db: Database session
        
    Returns:
        Updated {model_name} instance if found, None otherwise
    '''
    result = await db.execute(
        select({model_name}DB).where({model_name}DB.id == {model_name.lower()}_id)
    )
    db_{model_name.lower()} = result.scalar_one_or_none()
    
    if not db_{model_name.lower()}:
        return None
    
    update_data = {model_name.lower()}_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_{model_name.lower()}, field, value)
    
    await db.commit()
    await db.refresh(db_{model_name.lower()})
    return {model_name}.model_validate(db_{model_name.lower()})
"""
    
    def _generate_python_delete(self, model_name: str, schema: Dict[str, Any]) -> str:
        """Generate Python DELETE operation."""
        return f"""async def delete_{model_name.lower()}(
    {model_name.lower()}_id: str,
    db: AsyncSession
) -> bool:
    '''
    Delete a {model_name}.
    
    Args:
        {model_name.lower()}_id: ID of the {model_name} to delete
        db: Database session
        
    Returns:
        True if deleted, False if not found
    '''
    result = await db.execute(
        select({model_name}DB).where({model_name}DB.id == {model_name.lower()}_id)
    )
    db_{model_name.lower()} = result.scalar_one_or_none()
    
    if not db_{model_name.lower()}:
        return False
    
    await db.delete(db_{model_name.lower()})
    await db.commit()
    return True
"""
    
    # Private helper methods for TypeScript code generation
    def _generate_typescript_create(self, model_name: str, schema: Dict[str, Any]) -> str:
        """Generate TypeScript CREATE operation."""
        return f"""export async function create{model_name}(
  {model_name.lower()}: {model_name}
): Promise<{model_name}> {{
  const response = await fetch('/{model_name.lower()}s', {{
    method: 'POST',
    headers: {{ 'Content-Type': 'application/json' }},
    body: JSON.stringify({model_name.lower()})
  }});
  
  if (!response.ok) {{
    throw new Error(`Failed to create {model_name.lower()}`);
  }}
  
  return response.json();
}}
"""
    
    def _generate_typescript_read(self, model_name: str, schema: Dict[str, Any]) -> str:
        """Generate TypeScript READ operation."""
        return f"""export async function get{model_name}(
  id: string
): Promise<{model_name} | null> {{
  const response = await fetch(`/{model_name.lower()}s/${{id}}`);
  
  if (response.status === 404) {{
    return null;
  }}
  
  if (!response.ok) {{
    throw new Error(`Failed to get {model_name.lower()}`);
  }}
  
  return response.json();
}}

export async function list{model_name}s(
  skip: number = 0,
  limit: number = 100
): Promise<{model_name}[]> {{
  const response = await fetch(`/{model_name.lower()}s?skip=${{skip}}&limit=${{limit}}`);
  
  if (!response.ok) {{
    throw new Error(`Failed to list {model_name.lower()}s`);
  }}
  
  return response.json();
}}
"""
    
    def _generate_typescript_update(self, model_name: str, schema: Dict[str, Any]) -> str:
        """Generate TypeScript UPDATE operation."""
        return f"""export async function update{model_name}(
  id: string,
  {model_name.lower()}Update: Partial<{model_name}>
): Promise<{model_name} | null> {{
  const response = await fetch(`/{model_name.lower()}s/${{id}}`, {{
    method: 'PUT',
    headers: {{ 'Content-Type': 'application/json' }},
    body: JSON.stringify({model_name.lower()}Update)
  }});
  
  if (response.status === 404) {{
    return null;
  }}
  
  if (!response.ok) {{
    throw new Error(`Failed to update {model_name.lower()}`);
  }}
  
  return response.json();
}}
"""
    
    def _generate_typescript_delete(self, model_name: str, schema: Dict[str, Any]) -> str:
        """Generate TypeScript DELETE operation."""
        return f"""export async function delete{model_name}(
  id: string
): Promise<boolean> {{
  const response = await fetch(`/{model_name.lower()}s/${{id}}`, {{
    method: 'DELETE'
  }});
  
  if (response.status === 404) {{
    return false;
  }}
  
  if (!response.ok) {{
    throw new Error(`Failed to delete {model_name.lower()}`);
  }}
  
  return true;
}}
"""
    
    # Private helper methods for SQL code generation
    def _generate_sql_create(self, model_name: str, schema: Dict[str, Any]) -> str:
        """Generate SQL CREATE TABLE statement."""
        properties = self.get_properties(schema)
        required = self.get_required_fields(schema)
        
        columns = []
        for prop_name, prop_def in properties.items():
            sql_type = self._json_type_to_sql(prop_def.get('type', 'string'))
            nullable = "NOT NULL" if prop_name in required else "NULL"
            
            column_def = f"    {prop_name} {sql_type} {nullable}"
            if prop_name == 'id':
                column_def += " PRIMARY KEY"
            
            columns.append(column_def)
        
        columns_str = ",\n".join(columns)
        return f"""CREATE TABLE {model_name.lower()}s (
{columns_str}
);

CREATE INDEX idx_{model_name.lower()}s_id ON {model_name.lower()}s(id);
"""
    
    def _generate_sql_read(self, model_name: str, schema: Dict[str, Any]) -> str:
        """Generate SQL SELECT statements."""
        return f"""-- Get single {model_name.lower()} by ID
SELECT * FROM {model_name.lower()}s WHERE id = :id;

-- List all {model_name.lower()}s with pagination
SELECT * FROM {model_name.lower()}s 
ORDER BY id 
LIMIT :limit OFFSET :offset;

-- Count total {model_name.lower()}s
SELECT COUNT(*) FROM {model_name.lower()}s;
"""
    
    def _generate_sql_update(self, model_name: str, schema: Dict[str, Any]) -> str:
        """Generate SQL UPDATE statement."""
        properties = self.get_properties(schema)
        set_clauses = [f"{prop} = :{prop}" for prop in properties.keys() if prop != 'id']
        
        return f"""UPDATE {model_name.lower()}s
SET
    {',\n    '.join(set_clauses)}
WHERE id = :id;
"""
    
    def _generate_sql_delete(self, model_name: str, schema: Dict[str, Any]) -> str:
        """Generate SQL DELETE statement."""
        return f"""DELETE FROM {model_name.lower()}s WHERE id = :id;
"""
    
    def _json_type_to_sql(self, json_type: str) -> str:
        """Convert JSON schema type to SQL type."""
        type_mapping = {
            'string': 'VARCHAR(255)',
            'integer': 'INTEGER',
            'number': 'DECIMAL',
            'boolean': 'BOOLEAN',
            'array': 'JSONB',
            'object': 'JSONB',
        }
        return type_mapping.get(json_type, 'TEXT')
