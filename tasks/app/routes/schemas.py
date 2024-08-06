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

user_with_project_schema = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string",
            "pattern": r'^[A-Z][a-z]+$'
        },
        "email": {
            "type": "string",
            "pattern": r'[\w\.-]+@(gmail.com|wp.pl|onet.pl)$'
        },
        "password": {
            "type": "string",
            "pattern": r'[\w\.-]+$'
        },
        "project_name": {
            "type": "string",
        },
        "project_description": {
            "type": "string",
        }
    },
    "required": ["username", "email", "project_name", "password", "project_description"]
}

project_with_task_schema = {
    "type": "object",
    "properties": {
        "project_name": {
            "type": "string",
        },
        "project_description": {
            "type": "string",
        },
        "user_id": {
            "type": "integer",
        },
        "task_title": {
            "type": "string",
        },
        "task_status": {
            "type": "string",
            "enum": ["NEW", "IN_PROGRESS", "COMPLETED"]
        },
    },
    "required": ["project_name", "project_description", "user_id", "task_title"]
}


def validate_email(email: str) -> bool:
    if not re.match(r'[\w\\.-]+@(gmail.com|wp.pl|onet.pl)$', email):
        return False
    return True


def validate_name(name: str) -> bool:
    if not re.match(r'^[A-Z][a-z]+$', name):
        return False
    return True
