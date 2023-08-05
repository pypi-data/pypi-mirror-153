class INCIDENT:
    def __init__(self, sno:str, name:str, type:str) -> None:
        self.id: str = str(sno)
        self.incident_name: str = str(name)
        self.incident_type: str = str(type)

    def __str__(self) -> str:
        return f"{self.id}, {self.incident_name}, {self.incident_type} "


class CMO:
    def __init__(self):
        self.incidents: list[INCIDENT] = []

    def get_incidents(self) -> list[INCIDENT]:
        incident1 = INCIDENT("100", "tripped", "accident")
        incident2 = INCIDENT("101", "fight", "accident")
        self.incidents.append(incident1)
        self.incidents.append(incident2)
        return self.incidents
