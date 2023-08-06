from enum import IntFlag

class BasicVariablePropertyMask(IntFlag):

    Unspecified = 0,

    Name = 1,

    Description = 1,

    TagType = 2,

    RealTimeEnabled = 4,

    DeadBandFilter = 8,

    DeadBandUnit = 16,

    Eu = 32,

    LowLimit = 64, 

    HighLimit = 128,

    ScaleEnable = 256,

    InputLowLimit = 512,

    InputHighLimit = 1024,

    Clamping = 2048,

    Domain = 4096,

    Interface = 8192,

    IoTagAddress = 16384,

    ProcessingEnabled = 32768,

    IsRecording = 65536,

    IsCompressing = 131072,

    StoreMillisecondsEnabled = 262144,

    StorageSet = 524288,




