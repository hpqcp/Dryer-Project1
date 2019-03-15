class HisEntity:
    LineName=""
    StageName=""
    ProcessName=""
    ParameterName=""
    HisDf=None

    def __init__(self, LineName, StageName, ProcessName, ParameterName, HisDf):
        self.LineName = LineName
        self.StageName = StageName
        self.ProcessName = ProcessName
        self.ParameterName = ParameterName
        self.HisDf = HisDf
