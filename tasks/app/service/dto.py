class UserWithProjectDto:
    username: str
    email: str
    password: str
    project_name: str
    project_description: str


class ProjectWithUserIdDto:
    name: str
    description: str
    user_id: int
