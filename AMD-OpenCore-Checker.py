import os,time,sys,plistlib

class occhecker:

    def __init__(self):
        self.drivers = ['FwRuntimeServices.efi', 'ApfsDriverLoader.efi', 'HFSPlus.efi']
        self.kexts = ['Lilu.kext', 'WhateverGreen.kext']
        self.bootfiles = 'BOOTX64.efi'
        self.ocfolder = ['ACPI', 'Drivers', 'Kexts', 'Tools', 'config.plist', 'OpenCore.efi']
        self.configstruc = {
            'ACPI': ['Add', 'Block', 'Patch', 'Quirks'],
            'Booter': ['Quirks'],
            'DeviceProperties': ['Add', 'Block'],
            'Kernel': ['Add', 'Block', 'Emulate', 'Patch', 'Quirks'],
            'Misc': ['BlessOverride', 'Boot', 'Debug', 'Entries', 'Security', 'Tools'],
            'NVRAM': ['Add', 'Block', 'LegacyEnable', 'LegacySchema'],
            'PlatformInfo': ['Automatic', 'Generic', 'UpdateDataHub', 'UpdateNVRAM', 'UpdateSMBIOS', 'UpdateSMBIOSMode'],
            'UEFI': ['ConnectDrivers', 'Drivers', 'Input', 'Protocols', 'Quirks']
        }
        self.error = []
        self.warning = []
        self.acpi = ['Add','Block','Patch','Quirks']
        self.booter = ['Quirks']
        self.deviceproperties = ['Add','Block']
        self.kernel = ['Add','Block','Emulate','Patch','Quirks']
        self.misc = ['BlessOverride','Boot','Debug','Entries','Security','Tools']
        self.nvram = ['Add','Block']
        self.platforminfo = ['Automatic','Generic','UpdateDataHub','UpdateNVRAM','UpdateSMBIOS','UpdateSMBIOSMode']
        self.uefi = ['ConnectDrivers','Drivers','Input','Protocols','Quirks']
        self.quirks = {
            'Booter': {
                'AvoidRuntimeDefrag': True,
                'EnableSafeModeSlide': True,
                'EnableWriteUnprotector': True,
                'ProvideCustomSlide': True,
                'SetupVirtualMap': True,
            }, 
            'Kernel': {
                'DummyPowerManagement': True,
                'DisableIoMapper': True,
                'PanicNoKextDump': True,
                'PowerTimeoutKernelPanic': True
            }, 
            'UEFI': {
                'ExitBootServicesDelay': 0,
                'RequestBootVarFallback': True,
                'RequestBootVarRouting': True,
                'ProvideConsoleGop': True
            }
        }
        self.others = {
            'Misc': {
                'Boot': {
                    'HibernateMode': 'None',
                    'HideSelf': True,
                    'UsePicker': True
                },
                'Debug': {
                    'DisableWatchDog': True
                },
                'Security': {
                    'RequireSignature': False,
                    'RequireVault': False,
                    'ScanPolicy': 0
                }
            },
            'PlatformInfo': {
                'Automatic': True,
                'UpdateDataHub': True,
                'UpdateNVRAM': True,
                'UpdateSMBIOS': True,
                'UpdateSMBIOSMode': 'Create'
            },
            'UEFI': {
                'ConnectDrivers': True,
                'Protocols': {
                    'ConsoleControl': True
                }
            }
        }
        self.folders = {
            'ACPI': 'ACPI',
            'Kernel': 'Kexts'
        }
        self.suffix = {
            'ACPI': '.aml',
            'Kernel': '.kext'
        }
        self.paths = {
            'ACPI': 'Path',
            'Kernel': 'BundlePath'
        }
    
    def pred(self, string):
        return('\033[1;91m{}\033[00m'.format(string))

    def pgreen(self, string):
        return('\033[1;92m{}\033[00m'.format(string))

    def pgray(self, string):
        return('\033[1;90m{}\033[00m'.format(string))
    
    def pyellow(self, string):
        return('\033[1;93m{}\033[00m'.format(string))

    def clear(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def title(self, t):
        print('-'*50)
        print('{:^50s}'.format(t))
        print('-'*50)

    def info(self):
        self.clear()
        # Let's start by adding a title
        self.title('Checking if the current folder is OC folder...')
        print('')
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        isOCfolder = True
        for d in self.ocfolder:
            if not os.path.exists(d):
                isOCfolder = False
        time.sleep(0.1)
        if isOCfolder:
            print(self.pgreen('OK'))
        else:
            print(self.pgray('Nope'))
        time.sleep(0.1)
        self.clear()
        self.title('Gathering information...')
        print('')
        if not isOCfolder:
            print('Please paste the path of the EFI folder: ', end='')
            self.efiloc = input('').replace('\\', '')
            if self.efiloc.endswith(' '):
                self.efiloc = self.efiloc[:-1]
            os.chdir(self.efiloc)
        else:
            os.chdir('../')

    def checkfiles(self):
        # Now we are in the OC folder
        # We can finally do something now
        # Let's check some required files first
        self.clear()
        self.title('Checking OpenCore files and folders...')

        # Check folder structure
        print('')
        print('Checking root folder structure... ', end='')
        if os.path.exists('./BOOT') and os.path.exists('./OC'):
            print(self.pgreen('OK'))
        else:
            print(self.pred('Error'))
            print('')
            print(self.pred('Wrong folder structure!'))
            print(self.pred('Missing a folder'))
            print('')
            input('Press any key to exit... ')
            sys.exit()
        time.sleep(0.01)

        print('Checking BOOT folder... ', end='')
        if os.path.exists('./BOOT/BOOTX64.efi'):
            print(self.pgreen('OK'))
        else:
            print(self.pred('Error'))
            print(self.pred('   Missing BOOTX64.efi'))
            self.error.append('Missing BOOTX64.efi')
        time.sleep(0.01)

        print('Checking OC folder...')
        os.chdir('./OC')
        for d in self.ocfolder:
            print(' - {}... '.format(d),end='')
            if not os.path.exists(d):
                print(self.pred('Error'))
                print(self.pred('Missing {}'.format(d)))
                input('Press any key to exit...')
                sys.exit()
            print(self.pgreen('OK'))
            time.sleep(0.01)
        time.sleep(0.01)

        print('Checking needed kexts in Kexts folder...')
        os.chdir('./Kexts')
        for k in self.kexts:
            print(' - {}... '.format(k),end='')
            if os.path.exists(k):
                print(self.pgreen('OK'))
            else:
                print(self.pred('Error'))
                print(self.pred('Missing {}'.format(k)))
                self.error.append('Missing {}'.format(k))
            time.sleep(0.01)
        print(' - {}... '.format('FakeSMC.kext or VirtualSMC.kext'),end='')
        if os.path.exists('FakeSMC.kext') or os.path.exists('VirtualSMC.kext'):
            print(self.pgreen('OK'))
        else:
            print(self.pred('Warning'))
            print(self.pyellow('   Missing FakeSMC.kext or VirtualSMC.kext'))
            self.warning.append('Missing FakeSMC.kext or VirtualSMC.kext in Kexts folder')
        time.sleep(0.01)

        print('Checking needed drivers in Drivers folder...')
        os.chdir('../Drivers')
        for d in self.drivers:
            print(' - {}... '.format(d), end='')
            if os.path.exists(d):
                print(self.pgreen('OK'))
            else:
                print(self.pred('Warning'))
                print(self.pyellow('   Missing {}'.format(d)))
                self.warning.append('Missing {} in Drivers folder'.format(d))
            time.sleep(0.01)
        print(self.pgreen('Done'))
        time.sleep(0.1)
        os.chdir('../')

    def checkpliststc(self):
        self.clear()
        self.title('Checking config.plist structure...')
        print('')
        print('Loading config.plist... ', end='')
        c = open('config.plist', 'rb')
        self.config = plistlib.load(c)
        print(self.pgreen('Done'))
        time.sleep(0.01)

        print('Checking root config structure...')
        for x in self.configstruc:
            print(' - {}... '.format(x),end='')
            if x in self.config:
                print(self.pgreen('OK'))
            else:
                print(self.pred('Error'))
                print(self.pred('   Missing {} in config.plist'.format(x)))
                self.error.append('Missing {} in config.plist'.format(x))
            time.sleep(0.01)

        for p in self.configstruc:
            print('Checking {} structure... '.format(p))
            if p in self.config:
                for x in self.configstruc[p]:
                    print(' - {} > {}... '.format(p,x),end='')
                    if x in self.config[p]:
                        print(self.pgreen('OK'))
                    else:
                        print(self.pred('Error'))
                        print(self.pred('Missing {} -> {} in config.plist'.format(p,x)))
                        self.error.append('Missing {} -> {} in config.plist'.format(p,x))
                    time.sleep(0.01)
            else:
                print(self.pgray('Skipped because of missing {}'.format(p)))
                time.sleep(0.01)
        print(self.pgreen('Done'))
        time.sleep(0.1)

    def checkquirks(self):
        self.clear()
        self.title('Checking Quirks... ')
        print('')
        for q in self.quirks:
            if q in self.config:
                print('Checking {} > Quirks'.format(q))
                for quirk in self.quirks[q]:
                    print(' - Checking {} > Quirks > {}... '.format(q,quirk), end='')
                    if quirk in self.config[q]['Quirks']:
                        if self.quirks[q][quirk] == self.config[q]['Quirks'][quirk]:
                            print(self.pgreen('OK'))
                        else:
                            print(self.pred('Error'))
                            print(self.pred('   {} > Quirks > {} should be set to {}'.format(q,quirk, self.quirks[q][quirk])))
                            self.error.append('{} > Quirks > {} should be set to {}'.format(q,quirk, self.quirks[q][quirk]))
                    else:
                        print(self.pred('Error'))
                        print(self.pred('   Missing {} > Quirks > {} in config.plist and should be set to {}'.format(q,quirk,self.quirks[q][quirk])))
                        self.error.append('Missing {} > Quirks > {} in config.plist and should be set to {}'.format(q,quirk,self.quirks[q][quirk]))
                    time.sleep(0.01)
            else:
                print(self.pgray('Skipping {} part because of missing {} in config.plist...'.format(q,q)))
                time.sleep(0.01)
        print(self.pgreen('Done'))
        time.sleep(0.1)

    def checkaddpath(self):
        self.clear()
        self.title('Checking Add Paths...')
        print('')
        self.filtered_files = {}
        for folder in self.folders:
            files = os.listdir(self.folders[folder])
            temp_array=[]
            for f in files:
                if f.endswith(self.suffix[folder]) and not f.startswith('._'):
                    temp_array.append(f)
            self.filtered_files[folder] = temp_array
        for folder in self.folders:
            if folder in self.config:
                print('Checking {} folder -> {} > Add... '.format(self.folders[folder],folder),end='')
                if self.filtered_files[folder] != []:
                    print('')
                    for f in self.filtered_files[folder]:
                        b = False
                        print(' - Checking {}... '.format(f),end='')
                        for item in self.config[folder]['Add']:
                            if item[self.paths[folder]] == f:
                                b = True
                                if 'Enabled' in item:
                                    if not item['Enabled']:
                                        print(self.pred('Warning'))
                                        print(self.pyellow('   Enabled is not set to True in {} > Add > {}'.format(folder,f)))
                                        self.warning.append('Enabled is not set to True in {} > Add > {}'.format(folder,f))
                                    else:
                                        print(self.pgreen('OK'))
                                else:
                                    print(self.pyellow('Warning'))
                                    print(self.pyellow('    Missing Enable in {} > Add > {}'.format(folder,f)))
                                    self.warning.append('Missing Enable in {} > Add > {}'.format(folder,f))
                                break
                        if not b:
                            print(self.pred('Warning'))
                            print(self.pyellow('   Missing {} in {} > Add'.format(folder,f)))
                            self.warning.append('Missing {} in {} > Add'.format(folder,f))
                        time.sleep(0.01)
                else:
                    print(self.pgray('Skipped'))
                    time.sleep(0.01)
                print('Checking {} > Add -> {} folder... '.format(folder,self.folders[folder]), end='')
                if self.config[folder]['Add'] != []:
                    print('')
                    for item in self.config[folder]['Add']:
                        if item['Enabled']:
                            print(' - Checking {}... '.format(item[self.paths[folder]]), end='')
                            if item[self.paths[folder]] not in self.filtered_files[folder]:
                                print(self.pred('Error'))
                                print(self.pred('   Enabled {} in config.plist which does not exist'.format(item[self.paths[folder]])))
                                self.error.append('Enabled {} in config.plist which does not exist'.format(item[self.paths[folder]]))
                            else:
                                print(self.pgreen('OK'))
                        time.sleep(0.01)
                else:
                    print(self.pgray('Skipped'))
                    time.sleep(0.01)
            else:
                print(self.pgray('Skipping {} > Add because of missing {} in config.plist'.format(folder,folder)))
                time.sleep(0.01)
        print(self.pgreen('Done'))
        time.sleep(0.1)

    def checkkernel(self):
        checklist = ['ExecutablePath', 'PlistPath']
        self.clear()
        for check in checklist:
            self.title('Checking {} in Kernel > Add...'.format(check))
            print('')
            os.chdir('./Kexts')
            kexts = self.filtered_files['Kernel']
            if 'Kernel' in self.config:
                print('Checking Kernel > Add -> Kexts folder... ',end='')
                if self.config['Kernel']['Add'] != []:
                    print('')
                    for item in self.config['Kernel']['Add']:
                        print(' - Checking {}... '.format(item['BundlePath']), end='')
                        if check in item:
                            kextbundle = item['BundlePath']
                            kextcheck = item[check]
                            if kextcheck != '':
                                if os.path.isfile('{}/{}'.format(kextbundle,kextcheck)):
                                    print(self.pgreen('OK'))
                                else:
                                    print(self.pred('Error'))
                                    print(self.pred('   {} under {} is set which does not exist'.format(check,kextbundle)))
                                    self.error.append('{} under {} is set which does not exist'.format(check,kextbundle))
                            else:
                                print(self.pgray('Skipped'))
                        else:
                            print(self.pgray('Skipped'))
                        time.sleep(0.01)
                else:
                    print(self.pgray('Skipped'))
                print('Checking Kexts folder -> Kernel > Add... ',end='')
                if kexts != []:
                    print('')
                    for kext in kexts:
                        print(' - Checking {}... '.format(kext), end='')
                        kextbundle = kext
                        kextcheck = 'Contents/MacOS/{}'.format(kext[:-5]) if check == 'ExecutablePath' else 'Contents/Info.plist'
                        if os.path.isfile('{}/{}'.format(kextbundle,kextcheck)):
                            b = False
                            for item in self.config['Kernel']['Add']:
                                if kextcheck == item[check] and kextbundle == item['BundlePath']:
                                    b = True
                                    break
                            if b:
                                print(self.pgreen('OK'))
                            else:
                                print(self.pred('Error'))
                                print(self.pred('   {} has an {} but not set in config.plist'.format(kextbundle, 'executable file' if check == 'ExecutablePath' else 'info.plist')))
                                self.error.append('{} has an {} but not set in config.plist'.format(kextbundle, 'executable file' if check == 'ExecutablePath' else 'info.plist'))
                        else:
                            print(self.pgray('Skipped'))
                        time.sleep(0.01)
                else:
                    print(self.pgray('Skipped'))
            else:
                print(self.pgray('Skipped because of missing Kernel in config.plist'))
            print(self.pgreen('Done'))
            time.sleep(0.1)
            os.chdir('../')
            self.clear()

    def checktools(self):
        self.clear()
        self.title('Checking Tools...')
        print('')
        time.sleep(0.01)
        unfiltered_tools = os.listdir('Tools')
        tools = []
        for tool in unfiltered_tools:
            if tool.endswith('.efi') and not tool.startswith('._'):
                tools.append(tool)
        if 'Misc' in self.config:
            print('Checking Misc > Tools -> Tools... ',end='')
            if self.config['Misc']['Tools'] != []:
                print('')
                n = 0
                for tool in self.config['Misc']['Tools']:
                    print(' - Checking {}... '.format(tool['Path']), end='')
                    if 'Path' in tool and 'Enabled' in tool:
                        path = tool['Path']
                        if path in tools:
                            if tool['Enabled']:
                                print(self.pgreen('OK'))
                            else:
                                print(self.pred('Error'))
                                print(self.pred('   Disabled {} which exists in Tools'.format(path)))
                                self.error.append('Disabled {} which exists in Tools'.format(path))
                        elif tool['Enabled']:
                            print(self.pred('Error'))
                            print(self.pred('   Enabled {} which does not exist in Tools'.format(path)))
                            self.error.append('Enabled {} which does not exist in Tools'.format(path))
                        else:
                            print(self.pgreen('OK'))
                    else:
                        print(self.pred('Error'))
                        print(self.pred('   Item {} is not set properly (missing Path or Enabled)'.format(n)))
                        self.error.append('Item {} is not set properly (missing Path or Enabled)'.format(n))
                    n += 1
                    time.sleep(0.01)
            else:
                print(self.pgray('Skipped'))
                time.sleep(0.01)
            print('Checking Tools -> Misc > Tools... ',end='')
            if tools != []:
                print('')
                for tool in tools:
                    print(' - Checking {}... '.format(tool), end='')
                    b = False
                    for item in self.config['Misc']['Tools']:
                        if 'Enabled' in item and 'Path' in item:
                            if tool == item['Path'] and item['Enabled']:
                                b = True
                                break
                    if b:
                        print(self.pgreen('OK'))
                    else:
                        print(self.pred('Error'))
                        print(self.pred('   {} exists in Tools folder but not set properly in config.plist'.format(tool)))
                        self.error.append('{} exists in Tools folder but not set properly in config.plist'.format(tool))
            else:
                print(self.pgray('Skipped'))
        else:
            print(self.pgray('Skipped because of missing Misc in config.plist'))
        print(self.pgreen('Done'))
        time.sleep(0.1)

    def checkdrivers(self):
        self.clear()
        self.title('Checking Drivers...')
        print('')
        if 'UEFI' in self.config:
            print('Checking UEFI > Drivers -> Drivers... ',end='')
            if 'Drivers' in self.config['UEFI']:
                print('')
                unfiltered_drivers = os.listdir('./Drivers')
                drivers = []
                for driver in unfiltered_drivers:
                    if driver.endswith('.efi') and not driver.startswith('._'):
                        drivers.append(driver)
                for driver in self.config['UEFI']['Drivers']:
                    print(' - Checking {}... '.format(driver), end='')
                    if driver in drivers:
                        print(self.pgreen('OK'))
                    else:
                        print(self.pred('Error'))
                        print(self.pred('   Injected {} in UEFI > Drivers which does not exist in Drivers folder'.format(driver)))
                        self.error.append('Injected {} in UEFI > Drivers which does not exist in Drivers folder'.format(driver))
                    time.sleep(0.01)
                for driver in drivers:
                    print(' - Checking {}... '.format(driver), end='')
                    b = False
                    for item in self.config['UEFI']['Drivers']:
                        if driver == item:
                            b = True
                            break
                    if b:
                        print(self.pgreen('OK'))
                    else:
                        print(self.pred('Error'))
                        print(self.pred('   Missing {} in config.plist'.format(driver)))
                        self.error.append('Missing {} in config.plist'.format(driver))
                    time.sleep(0.01)
            else:
                print(self.pgray('Skipped'))
                time.sleep(0.01)
        else:
            print(self.pgray('Skipped because of missing UEFI in config.plist'))
        print(self.pgreen('Done'))
        time.sleep(0.1)
            
    def checkemulate(self):
        self.clear()
        self.title('Checking Kernel Emulate...')
        print('')
        print('Checking Kernel > Emulate... ',end='')
        if 'Kernel' in self.config:
            if 'Emulate' in self.config['Kernel']:
                if self.config['Kernel']['Emulate'] == {}:
                    print(self.pgreen('OK'))
                elif 'CpuidMask' in self.config['Kernel']['Emulate']:
                    if self.config['Kernel']['Emulate']['CpuidMask'] == b'':
                        print(self.pgreen('OK'))
                    else:
                        print(self.pred('Error'))
                        print(self.pred('Kernel > Emulate > CpuidMask should be empty'))
                        self.error.append('Kernel > Emulate > CpuidMask should be empty')
                elif 'CpuidData' in self.config['Kernel']['Emulate']:
                    if self.config['Kernel']['Emulate']['CpuidData'] == b'':
                        print(self.pgreen('OK'))
                    else:
                        print(self.pred('Error'))
                        print(self.pred('Kernel > Emulate > CpuidData should be empty'))
                        self.error.append('Kernel > Emulate > CpuidData should be empty')
                else:
                    print(self.pred('Error'))
                    print(self.pred('Emulate should be empty'))
                    self.error.append('Emulate should be empty')
            else:
                print(self.pgreen('OK'))
        else:
            print('')
            print(self.pgray('Skipped because of missing Kernel in config.plist'))
        time.sleep(0.1)

    def checkother(self):
        self.clear()
        self.title('Checking other stuffs')
        print('')
        print('Checking Misc... ',end='')
        if 'Misc' in self.config:
            print('')
            for part in self.others['Misc']:
                print(' - Checking Misc > {}... '.format(part),end='')
                if part in self.config['Misc']:
                    print('')
                    for setting in self.others['Misc'][part]:
                        print('  - Checking Misc > {} > {}... '.format(part, setting),end='')
                        if setting in self.config['Misc'][part]:
                            if self.config['Misc'][part][setting] == self.others['Misc'][part][setting]:
                                print(self.pgreen('OK'))
                            else:
                                print(self.pred('Error'))
                                print(self.pred('    Misc > {} > {} should be set to {}'.format(part, setting, self.others['Misc'][part][setting])))
                                self.error.append('Misc > {} > {} should be set to {}'.format(part, setting, self.others['Misc'][part][setting]))
                        else:
                            print(self.pred('Error'))
                            print(self.pred('    Missing Misc > {} > {} and should be set to {}'.format(part, setting, self.others['Misc'][part][setting])))
                            self.error.append('Missing Misc > {} > {} should be set to {}'.format(part, setting, self.others['Misc'][part][setting]))
                        time.sleep(0.01)
                else:
                    print(self.pgray('Skipped because of missing Misc > {} in config.plist'.format(part)))
                    time.sleep(0.01)
        else:
            print(self.pgray('SkIpPeD'))
            print(self.pgray('SkIpPeD bEcAuSe Of MiSsInG Misc iN config.plist'))
            time.sleep(0.01)
        time.sleep(0.1)
        self.clear()
        self.title('Checking other stuffs')
        print('')
        print('Checking PlatformInfo... ',end='')
        if 'PlatformInfo' in self.config:
            print('')
            for setting in self.others['PlatformInfo']:
                print(' - Checking PlatformInfo > {}... '.format(setting),end='')
                if setting in self.config['PlatformInfo']:
                    if self.config['PlatformInfo'][setting] == self.others['PlatformInfo'][setting]:
                        print(self.pgreen('OK'))
                    else:
                        print(self.pred('Error'))
                        print(self.pred('   PlatformInfo > {} should be set to {}'.format(setting, self.others['PlatformInfo'][setting])))
                        self.error.append('PlatformInfo > {} should be set to {}'.format(setting, self.others['PlatformInfo'][setting]))
                else:
                    print(self.pred('Error'))
                    print(self.pred('   Missing PlatformInfo > {} and should be set to {}'.format(setting,self.others['PlatformInfo'][setting])))
                    self.error.append('Missing PlatformInfo > {} and should be set to {}'.format(setting, self.others['PlatformInfo'][setting]))
                time.sleep(0.01)
        else:
            print(self.pgray('Skipped'))
            print(self.pgray('Skipped because of missing PlatformInfo in config.plist'))
            time.sleep(0.01)
        time.sleep(0.1)
        self.clear()
        self.title('Checking other stuffs')
        print('')
        print('Checking UEFI... ',end='')
        if 'UEFI' in self.others:
            print('')
            for setting in self.others['UEFI']:
                print(' - Checking UEFI > {}... '.format(setting), end='')
                if setting in self.config['UEFI']:
                    if type(self.config['UEFI'][setting]) != dict:
                        if self.config['UEFI'][setting] == self.others['UEFI'][setting]:
                            print(self.pgreen('OK'))
                        else:
                            print(self.pred('Error'))
                            print(self.pred('   UEFI > {} should be set to {}'.format(setting, self.others['UEFI'][setting])))
                            self.error.append('UEFI > {} should be set to {}'.format(setting, self.others['UEFI'][setting]))
                    else:
                        print('')
                        for item in self.others['UEFI'][setting]:
                            print('   - Checking UEFI > {} > {}... '.format(setting, item),end='')
                            if item in self.config['UEFI'][setting]:
                                if self.config['UEFI'][setting][item] == self.others['UEFI'][setting][item]:
                                    print(self.pgreen('OK'))
                                else:
                                    print(self.pred('Error'))
                                    print(self.pred('   UEFI > {} > {} should be set to {}'.format(setting, item, self.others['UEFI'][setting][item])))
                                    self.error.append('UEFI > {} > {} should be set to {}'.format(setting, item, self.others['UEFI'][setting][item]))
                            else:
                                print(self.pred('Error'))
                                print(self.pred('   Missing UEFI > {} > {} and should be set to {}'.format(setting, item ,self.others['UEFI'][setting][item])))
                                self.error.append('Missing UEFI > {} > {} and should be set to {}'.format(setting, item, self.others['UEFI'][setting][item]))
                            time.sleep(0.01)
                else:
                    print(self.pred('Error'))
                    print(self.pred('   Missing UEFI > {} and should be set to {}'.format(setting, self.others['UEFI'][setting])))
                    self.error.append('Missing UEFI > {} and should be set to {}'.format(setting, self.others['UEFI'][setting]))
                time.sleep(0.01)
        else:
            print(self.pgray('Skipped'))
            print(self.pgray('Skipped because of missing UEFI in config.plist'))
                        

    def printerror(self):
        self.clear()
        self.title('Warnings and errors...')
        print('')
        print(self.pyellow('All warnings: '), end='')
        if self.warning != []:
            print('')
            for n in self.warning:
                print(self.pyellow(' - {}'.format(n)))
        else:
            print(self.pgreen('None'))
        print(self.pred('All errors: '), end='')
        time.sleep(0.1)
        if self.error != []:
            print('')
            for n in self.error:
                print(self.pred(' - {}'.format(n)))
        else:
            print(self.pgreen('None'))
        print('')

    def main(self):
        # Clear the window first
        self.clear()

        # We need to gather some information first
        self.info()

        # We now have the folder so we are going to check if all the files are in place
        self.checkfiles()

        # Load config.plist and check the structure
        self.checkpliststc()

        # Check all quirks settings
        self.checkquirks()

        # Check if all the Add path are set correctly
        self.checkaddpath()

        # Check Kernel part of config.plist
        self.checkkernel()

        # Check Tools and Drivers are injected correctly in config.plist
        self.checktools()
        self.checkdrivers()

        # Check other stuffs
        self.checkemulate()
        self.checkother()

        # Finished everything so print out all errors
        self.printerror()
        

if __name__ == '__main__':
    occhecker().main()