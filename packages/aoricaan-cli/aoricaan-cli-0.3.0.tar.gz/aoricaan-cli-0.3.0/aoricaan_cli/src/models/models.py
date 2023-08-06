from pydantic import BaseModel


class LambdaConfig(BaseModel):
    Code: str
    Handler: str
    Role: str
    Runtime: str
    FunctionName: str
    MemorySize: str
    Timeout: str
    Environment: str
    VpcConfig: str
    Layers: str
