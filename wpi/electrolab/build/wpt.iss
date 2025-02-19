; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Electrolab"
#define ModuleName "Verification"
#define MyAppVersion "2.0"
#define MyAppPublisher "Diposoft"
#define MyAppURL "http://diposoft.ru/ElectroLab.html"
#define MyAppExeName "wpt.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{51C6F430-E2B3-42FB-A704-43B2CC525D42}
;AppName={#MyAppName}
AppName={#ModuleName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName=c:\{#MyAppName}\{#ModuleName}
DefaultGroupName={#MyAppName}
OutputDir=C:\work\ElectroLab\branches\2.0\electrolab\build\dist
;OutputBaseFilename=IntegrationSetup
OutputBaseFilename=Setup_{#ModuleName}_{#MyAppVersion}
Compression=lzma
SolidCompression=yes

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Files]
;Source: "C:\work\ElectroLab\branches\2.0\electrolab\build\dist\wpt\integration.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\work\ElectroLab\branches\2.0\electrolab\build\dist\wpt\*"; DestDir: "{app}"; Excludes: "config.json,FastReport3.dll,psqlodbc.msi"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\work\ElectroLab\branches\2.0\electrolab\build\dist\wpt\config.json"; DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist uninsneveruninstall
Source: "C:\work\ElectroLab\branches\2.0\electrolab\build\dist\wpt\FastReport3.dll"; DestDir: "{syswow64}"; Flags: onlyifdoesntexist regserver uninsneveruninstall
Source: "C:\work\ElectroLab\branches\2.0\electrolab\build\dist\wpt\psqlodbc.msi"; DestDir: "{tmp}"; Flags: deleteafterinstall
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#ModuleName} {#MyAppVersion}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#ModuleName} {#MyAppVersion}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Config {#ModuleName} {#MyAppVersion}"; Filename: "notepad.exe"; WorkingDir: "{app}"; Parameters: "{app}\config.json"
Name: "{group}\Uninstall {#ModuleName} {#MyAppVersion}"; Filename: "{uninstallexe}"
Name: "{group}\Downloads"; Filename: "http://diposoft.ru/ElectroLab/install/"


[Run]
Filename: "msiexec.exe"; Parameters: "/passive TARGETDIR=""{sys}"" /i ""{tmp}\psqlodbc.msi"""
;Filename: "{app}\Schtasks / Create"; Parameters: "/x"
;Filename: "Schtasks"; Parameters: "/Create /tn ""Electrolab Integration"" /tr ""{app}\{#MyAppExeName} {app}\integration.ini"" /SC DAILY /ST 04:00:00"

[Registry]
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\ODBC Data Sources; ValueType: string; ValueName: PostgreSQL35W; ValueData: PostgreSQL Unicode; Flags: createvalueifdoesntexist uninsdeletevalue
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: Driver; ValueType: string; ValueData: {pf32}\psqlODBC\0900\bin\psqlodbc35w.dll
;Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: Driver; ValueType: string; ValueData: {sys}\psqlodbc35w.dll
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: CommLog; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: Debug; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: Fetch; ValueType: string; ValueData: 100
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: Optimizer; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: Ksqo; ValueType: string; ValueData: 1
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: UniqueIndex; ValueType: string; ValueData: 1
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: UseDeclareFetch; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: UnknownSizes; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: TextAsLongVarchar; ValueType: string; ValueData: 1
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: UnknownsAsLongVarchar; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: BoolsAsChar; ValueType: string; ValueData: 1
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: Parse; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: CancelAsFreeStmt; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: MaxVarcharSize; ValueType: string; ValueData: 255
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: MaxLongVarcharSize; ValueType: string; ValueData: 8190
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: ExtraSysTablePrefixes; ValueType: string; ValueData: dd_
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: Description; ValueType: string; ValueData: electrolab
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: Database; ValueType: string; ValueData: electrolab
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: Servername; ValueType: string; ValueData: localhost
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: Port; ValueType: string; ValueData: 5432
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: Username; ValueType: string; ValueData: electrolab
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: UID; ValueType: string; ValueData: electrolab
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: Password; ValueType: string; ValueData: electrolab
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: ReadOnly; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: ShowOidColumn; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: FakeOidIndex; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: RowVersioning; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: ShowSystemTables; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: Protocol; ValueType: string; ValueData: 7.4
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: ConnSettings; ValueType: string; ValueData: 
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: DisallowPremature; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: UpdatableCursors; ValueType: string; ValueData: 1
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: LFConversion; ValueType: string; ValueData: 1
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: TrueIsMinus1; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: BI; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: AB; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: ByteaAsLongVarBinary; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: UseServerSidePrepare; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: LowerCaseIdentifier; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: GssAuthUseGSS; ValueType: string; ValueData: 0
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: SSLmode; ValueType: string; ValueData: disable
Root: HKLM; SubKey: Software\ODBC\ODBC.INI\PostgreSQL35W; Flags: createvalueifdoesntexist uninsdeletevalue; ValueName: XaOpt; ValueType: string; ValueData: 1