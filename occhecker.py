import os,time,sys,plistlib

class occhecker:

    def __init__(self):
        self.drivers = ['FwRuntimeServices.efi', 'ApfsDriverLoader.efi', 'HFSPlus.efi']
        self.kexts = ['Lilu.kext', 'WhateverGreen.kext', 'NullCPUPowerManagement.kext']
        self.ocfiles = ['config.plist', 'OpenCore.efi']
        self.bootfiles = 'BOOTX64.efi'
        self.ocfolders = ['ACPI', 'Drivers', 'Kexts', 'Tools']
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
        self.acpi = ['Add','Block','Patch','Quirks']
        self.booter = ['Quirks']
        self.deviceproperties = ['Add','Block']
        self.kernel = ['Add','Block','Emulate','Patch','Quirks']
        self.misc = ['BlessOverride','Boot','Debug','Entries','Security','Tools']
        self.nvram = ['Add','Block']
        self.platforminfo = ['Automatic','Generic','UpdateDataHub','UpdateNVRAM','UpdateSMBIOS','UpdateSMBIOSMode']
        self.uefi = ['ConnectDrivers','Drivers','Input','Protocols','Quirks']
        self.quirks = {
            'ACPI': {
                'FadtEnableReset': False,
                'NormalizeHeaders': False,
                'RebaseRegions': False,
                'ResetHwSig': False,
                'ResetLogoStatus': False
            }, 
            'Booter': {
                'AvoidRuntimeDefrag': True,
                'DevirtualiseMmio': False,
                'DisableVariableWrite': False,
                'DiscardHibernateMap': False,
                'EnableSafeModeSlide': True,
                'EnableWriteUnprotector': True,
                'ForceExitBootServices': False,
                'ProtectCsmRegion': False,
                'ProvideCustomSlide': True,
                'SetupVirtualMap': True,
                'ShrinkMemoryMap': False,
            }, 
            'Kernel': {
                'AppleXcpmExtraMsrs': False,
                'CustomSMBIOSGuid': False,
                'DisableIoMapper': True,
                'PanicNoKextDump': True,
                'PowerTimeoutKernelPanic': True
            }, 
            'UEFI': {
                'AvoidHighAlloc': False,
                'ExitBootServicesDelay': 0,
                'IgnoreInvalidFlexRatio': False,
                'ProvideConsoleGop': True
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
        return("\033[1;91m{}\033[00m" .format(string))

    def pgreen(self, string):
        return("\033[1;92m{}\033[00m" .format(string))

    def pgray(self, string):
        return("\033[1;90m{}\033[00m" .format(string))

    def clear(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    
    def missing(self,s):
        print(self.pred('Error'))
        print(self.pred('Missing {}'.format(s)))

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
        for d in self.ocfolders:
            if not os.path.isdir(d):
                isOCfolder = False
        for f in self.ocfiles:
            if not os.path.isfile(f):
                isOCfolder = False
        time.sleep(0.05)
        self.clear()
        self.title('Gathering information...')
        print('')
        if isOCfolder == False:
            print('Please paste the path of the EFI folder: ', end='')
            self.efiloc = input('').replace('\\', '')
            if self.efiloc.endswith(' '):
                self.efiloc = self.efiloc[:-1]
            os.chdir(self.efiloc)
        self.checkfiles()

    def checkfiles(self):
        # Now we are in the OC folder
        # We can finally do something now
        # Let's check some required files first
        self.clear()
        self.title('Checking OpenCore files and folders...')

        # Check folder structure
        print('')
        print('Checking root folder structure... ', end='')
        if os.path.isdir('./BOOT') and os.path.isdir('./OC'):
            print(self.pgreen('OK'))
        else:
            print(self.pred('Error'))
            print('')
            print(self.pred('Wrong folder structure!'))
            print(self.pred('Probably missing a folder'))
            print('')
            input('Press any key to exit... ')
            sys.exit()
        time.sleep(0.05)

        print('Checking BOOT folder... ', end='')
        if os.path.isfile('./BOOT/BOOTX64.efi'):
            print(self.pgreen('OK'))
        else:
            self.missing(self.pred('BOOTX64.efi'))
        time.sleep(0.05)

        print('Checking OC folder...')
        os.chdir('./OC')
        for d in self.ocfolders:
            print(' - {}... '.format(d),end='')
            if not os.path.isdir(d):
                self.missing(self.pred(d))
                input('Press any key to exit...')
                sys.exit()
            print(self.pgreen('OK'))
            time.sleep(0.05)
        for f in self.ocfiles:
            print(' - {}... '.format(f),end='')
            if not os.path.isfile(f):
                self.missing(self.pred(f))
                input('Press any key to exit...')
                sys.exit()
            print(self.pgreen('OK'))
            time.sleep(0.05)
        time.sleep(0.05)

        print('Checking needed kexts in Kexts folder...')
        os.chdir('./Kexts')
        for k in self.kexts:
            print(' - {}... '.format(k),end='')
            if not os.path.isdir(k):
                self.missing(self.pred(k))
            print(self.pgreen('OK'))
            time.sleep(0.05)
        print(' - {}... '.format('FakeSMC.kext or VirtualSMC.kext'),end='')
        if not (os.path.isdir('FakeSMC.kext') or os.path.isdir('VirtualSMC.kext')):
            self.missing(self.pred('FakeSMC.kext or VirtualSMC.kext'))
            self.error.append('Missing FakeSMC.kext or VirtualSMC.kext in Kexts folder')
        else:
            print(self.pgreen('OK'))
        time.sleep(0.05)

        print('Checking needed drivers in Drivers folder...')
        os.chdir('../Drivers')
        for d in self.drivers:
            print(' - {}... '.format(d), end='')
            if not os.path.isfile(d):
                self.missing(self.pred(d))
                self.error.append('Missing {} in Drivers folder'.format(d))
            else:
                print(self.pgreen('OK'))
            time.sleep(0.05)
        time.sleep(0.5)
        print(self.pgreen('Done'))
        time.sleep(1)
        self.checkpliststc()

    def checkpliststc(self):
        self.clear()
        os.chdir('../')
        self.title('Checking config.plist structure...')
        print('')
        print('Loading config.plist... ', end='')
        c = open('config.plist', 'rb')
        self.config = plistlib.load(c)
        print(self.pgreen('Done'))
        time.sleep(0.05)

        print('Checking root config structure...')
        for x in self.configstruc:
            print(' - {}... '.format(x),end='')
            if not x in self.config:
                self.missing(self.pred('{} in config.plist'.format(x)))
                self.error.append('Missing {} in config.plist'.format(x))
            else:
                print(self.pgreen('OK'))
            time.sleep(0.05)

        for p in self.configstruc:
            print('Checking {} structure... '.format(p))
            if p in self.config:
                for x in self.configstruc[p]:
                    print(' - {}/{}... '.format(p,x),end='')
                    if not x in self.config[p]:
                        self.missing(self.pred('{}/{} in config.plist'.format(p,x)))
                        self.error.append('Missing {}/{} in config.plist'.format(p,x))
                    print(self.pgreen('OK'))
                    time.sleep(0.05)
            else:
                print(self.pred('Skipped because of missing {}'.format(p)))
                time.sleep(0.05)
        time.sleep(0.5)
        print(self.pgreen('Done'))
        time.sleep(1)
        self.checkquirks()

    def checkquirks(self):
        self.clear()
        self.title('Checking Quirks... ')
        print('')
        for q in self.quirks:
            if q in self.config:
                print('Checking {}/Quirks'.format(q))
                for quirk in self.quirks[q]:
                    print(' - Checking {}/Quirks/{}... '.format(q,quirk), end='')
                    if quirk in self.config[q]['Quirks']:
                        if self.quirks[q][quirk] == self.config[q]['Quirks'][quirk]:
                            print(self.pgreen('OK'))
                        else:
                            print(self.pred('Error'))
                            print(self.pred('   {}/Quirks/{} should be set to {}'.format(q,quirk, self.quirks[q][quirk])))
                            self.error.append('{}/Quirks/{} should be set to {}'.format(q,quirk, self.quirks[q][quirk]))
                    else:
                        print(self.pred('Error'))
                        print(self.pred('   Missing {}/Quirks/{} in config.plist'.format(q,quirk)))
                        self.error.append('Missing {}/Quirks/{} in config.plist'.format(q,quirk))
                    time.sleep(0.05)
            else:
                print(self.pred('Skipping {} part because of missing ACPI in config.plist...'.format(q)))
                time.sleep(0.05)
        time.sleep(0.5)
        print(self.pgreen('Done'))
        time.sleep(1)
        self.checkaddpath()
    
    

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
                print('Checking {} folder -> {}/Add... '.format(self.folders[folder],folder),end='')
                if self.filtered_files[folder] != []:
                    print('')
                    for f in self.filtered_files[folder]:
                        b = False
                        print(' - Checking {}... '.format(f),end='')
                        for item in self.config[folder]['Add']:
                            if item[self.paths[folder]] == f:
                                b = True
                                if 'Enabled' in item:
                                    if item['Enabled'] == False:
                                        print(self.pred('Error'))
                                        print(self.pred('   Enabled is not set to True in {}/Add/{}'.format(folder,f)))
                                        self.error.append('Enabled is not set to True in {}/Add/{}'.format(folder,f))
                                    else:
                                        print(self.pgreen('OK'))
                                else:
                                    print(self.pred('Error'))
                                    print(self.pred('    Enabled is not set in {}/Add/{}'.format(folder,f)))
                                    self.error.append('Enabled is not set in {}/Add/{}'.format(folder,f))
                                break
                        if b == False:
                            print(self.pred('Error'))
                            print(self.pred('   Missing {} in {}/Add'.format(folder,f)))
                            self.error.append('Missing {} in {}/Add'.format(folder,f))
                        time.sleep(0.05)
                else:
                    print(self.pgray('Skipped'))
                    time.sleep(0.05)
                print('Checking {}/Add -> {} folder... '.format(folder,self.folders[folder]), end='')
                if self.config[folder]['Add'] != []:
                    print('')
                    for item in self.config[folder]['Add']:
                        if item['Enabled'] == True:
                            print(' - Checking {}... '.format(item[self.paths[folder]]), end='')
                            if item[self.paths[folder]] not in self.filtered_files[folder]:
                                print(self.pred('Error'))
                                print(self.pred("   Enabled {} in config.plist which doesn't exist".format(item[self.paths[folder]])))
                                self.error.append("Enabled {} in config.plist which doesn't exist".format(item[self.paths[folder]]))
                            else:
                                print(self.pgreen('OK'))
                        time.sleep(0.05)
                else:
                    print(self.pgray('Skipped'))
                    time.sleep(0.05)
            else:
                print('Skipping {}/Add because of missing ACPI in config.plist'.format(folder))
                time.sleep(0.05)
        time.sleep(0.5)
        print(self.pgreen('Done'))
        time.sleep(1)
        self.checkkextexec()

    def checkkextexec(self):
        self.clear()
        self.title('Checking ExecutablePath in Kernel/Add...')
        print('')
        print('Checking Kernel/Add -> Kexts folder... ',end='')
        os.chdir('./Kexts')
        kexts = self.filtered_files['Kernel']
        if self.config['Kernel']['Add'] != []:
            print('')
            for item in self.config['Kernel']['Add']:
                print(' - Checking {}... '.format(item['BundlePath']), end='')
                if 'ExecutablePath' in item:
                    kextbundle = item['BundlePath']
                    kextexec = item['ExecutablePath']
                    if kextexec != '':
                        if os.path.isfile('{}/{}'.format(kextbundle,kextexec)):
                            print(self.pgreen('OK'))
                        else:
                            print(self.pred('Error'))
                            print(self.pred("   ExecutablePath under {} is set which doesn't exist".format(kextbundle)))
                            self.error.append("ExecutablePath under {} is set which doesn't exist".format(kextbundle))
                    else:
                        print(self.pgray('Skipped'))
                else:
                    print(self.pgray('Skipped'))
                time.sleep(0.05)
        else:
            print(self.pgray('Skipped'))
        print('Checking Kexts folder -> Kernel/Add... ',end='')
        if kexts != []:
            print('')
            for kext in kexts:
                print(' - Checking {}... '.format(kext), end='')
                kextbundle = kext
                kextexec = 'Contents/MacOS/{}'.format(kext[:-5])
                if os.path.isfile('{}/{}'.format(kextbundle,kextexec)):
                    b = False
                    for item in self.config['Kernel']['Add']:
                        if kextexec == item['ExecutablePath'] and kextbundle == item['BundlePath']:
                            b = True
                            break
                    if b == True:
                        print(self.pgreen('OK'))
                    else:
                        print(self.pred('Error'))
                        print(self.pred('   {} has an executable file but not set in config.plist'.format(kextbundle)))
                        self.error.append('{} has an executable file but not set in config.plist'.format(kextbundle))
                else:
                    print(self.pgray('Skipped'))
                time.sleep(0.05)
        else:
            print(self.pgray('Skipped'))
        time.sleep(0.5)
        print(self.pgreen('Done'))
        time.sleep(1)
        self.printerror()
            
    def printerror(self):
        self.clear()
        self.title('Errors...')
        print('')
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
        

if __name__ == "__main__":
    r = occhecker()
    r.main()