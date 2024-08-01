import re

email_and_password_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "pattern": r'[\w\.-]+@(gmail.com|wp.pl|onet.pl)$'
        },
        "password": {
            "type": "string",
            "pattern": r'[\w\.-]+$'
        }
    },
    "required": ["email", "password"]
}

name_and_password_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": r'^[A-Z][a-z]+$'
        },
        "password": {
            "type": "string",
            "pattern": r'[\w\.-]+$'
        }
    },
    "required": ["name", "password"]
}

name_password_and_email_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "pattern": r'[\w\.-]+@(gmail.com|wp.pl|onet.pl)$'
        },
        "password": {
            "type": "string",
            "pattern": r'[\w\.-]+$'
        },
        "name": {
            "type": "string",
            "pattern": r'^[A-Z][a-z]+$'
        }
    },
    "required": ["email", "password"]
}

user_id_and_description_schema = {
    "type": "object",
    "properties": {
        "user_id": {
            "type": "integer",
        },
        "description": {
            "type": "string",
        }
    },
    "required": ["user_id", "description"]
}

user_id_task_id_and_creation_data_schema = {
    "type": "object",
    "properties": {
        "user_id": {
            "type": "integer",
        },
        "task_id": {
            "type": "integer",
        },
        "creation_data": {
            "type": "string",
            "format": "date-time",
        }
    },
    "required": ["user_id", "task_id"]
}

status_and_project_id_schema = {
    "type": "object",
    "properties": {
        "project_id": {
            "type": "integer",
        },
        "status": {
            "type": "string",
            "enum": ["NEW", "IN_PROGRESS", "COMPLETED"]
        }
    },
    "required": ["project_id"]
}

status_schema = {
    "type": "object",
    "properties": {
        "status": {
            "type": "string",
            "enum": ["NEW", "IN_PROGRESS", "COMPLETED"]
        }
    },
    "required": ["status"]
}


def validate_email(email: str) -> bool:
    if not re.match(r'[\w\\.-]+@(gmail.com|wp.pl|onet.pl)$', email):
        return False
    return True
