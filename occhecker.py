import os,time,sys,plistlib

class occhecker:

    def __init__(self):
        self.drivers = ['FwRuntimeServices.efi', 'ApfsDriverLoader.efi', 'HFSPlus.efi']
        self.kexts = ['Lilu.kext', 'NullCPUPowerManagement.kext', 'WhateverGreen.kext']
        self.ocfiles = ['config.plist', 'OpenCore.efi']
        self.bootfiles = 'BOOTX64.efi'
        self.ocfolders = ['ACPI', 'Drivers', 'Kexts', 'Tools']
        # self.config = ['ACPI', 'Booter', 'DeviceProperties', 'Kernel', 'Misc', 'NVRAM', 'PlatformInfo', 'UEFI']
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
        self.acpiquirks = ['FadtEnableReset','NormalizeHeaders','RebaseRegions','ResetHwSig','ResetLogoStatus']
        self.acpiquirkset = {
            'FadtEnableReset': False,
            'NormalizeHeaders': False,
            'RebaseRegions': False,
            'ResetHwSig': False,
            'ResetLogoStatus': False
        }
        self.booterquirks = ['AvoidRuntimeDefrag','DevirtualiseMmio','DisableSingleUser','DisableVariableWrite','DiscardHibernateMap','EnableSafeModeSlide','EnableWriteUnprotector','ForceExitBootServices','ProtectCsmRegion','ProvideCustomSlide','SetupVirtualMap','ShrinkMemoryMap']
        self.booterquirkset = {
            'AvoidRuntimeDefrag': True,
            'DevirtualiseMmio': False,
            'DisableSingleUser': False,
            'DisableVariableWrite': False,
            'DiscardHibernateMap': False,
            'EnableSafeModeSlide': True
        }
    
    def pred(self, string):
        return("\033[1;91m{}\033[00m" .format(string))

    def pgreen(self, string):
        return("\033[1;92m{}\033[00m" .format(string))

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
        self.title('Gathering information...')
        print('')
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
        time.sleep(0.1)

        print('Checking BOOT folder... ', end='')
        if os.path.isfile('./BOOT/BOOTX64.efi'):
            print(self.pgreen('OK'))
        else:
            self.missing(self.pred('BOOTX64.efi'))
        time.sleep(0.1)

        print('Checking OC folder...')
        os.chdir('./OC')
        for d in self.ocfolders:
            print(' - {}... '.format(d),end='')
            if not os.path.isdir(d):
                self.missing(self.pred(d))
                input('Press any key to exit...')
                sys.exit()
            print(self.pgreen('OK'))
            time.sleep(0.1)
        for f in self.ocfiles:
            print(' - {}... '.format(f),end='')
            if not os.path.isfile(f):
                self.missing(self.pred(f))
                input('Press any key to exit...')
                sys.exit()
            print(self.pgreen('OK'))
            time.sleep(0.1)
        time.sleep(0.5)

        print('Checking needed kexts in Kexts folder...')
        os.chdir('./Kexts')
        for k in self.kexts:
            print(' - {}... '.format(k),end='')
            if not os.path.isdir(k):
                self.missing(self.pred(k))
            print(self.pgreen('OK'))
            time.sleep(0.1)
        print(' - {}... '.format('FakeSMC.kext or VirtualSMC.kext'),end='')
        if not (os.path.isdir('FakeSMC.kext') or os.path.isdir('VirtualSMC.kext')):
            self.missing(self.pred('FakeSMC.kext or VirtualSMC.kext'))
            self.error.append('Missing FakeSMC.kext or VirtualSMC.kext in Kexts folder')
        else:
            print(self.pgreen('OK'))
        time.sleep(0.5)

        print('Checking needed drivers in Drivers folder...')
        os.chdir('../Drivers')
        for d in self.drivers:
            print(' - {}... '.format(d), end='')
            if not os.path.isfile(d):
                self.missing(self.pred(d))
                self.error.append('Missing {} in Drivers folder'.format(d))
            else:
                print(self.pgreen('OK'))
            time.sleep(0.1)
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
        time.sleep(0.1)

        print('Checking root config structure...')
        for x in self.configstruc:
            print(' - {}... '.format(x),end='')
            if not x in self.config:
                self.missing(self.pred('{} in config.plist'.format(x)))
                self.error.append('Missing {} in config.plist'.format(x))
            else:
                print(self.pgreen('OK'))
            time.sleep(0.1)

        for p in self.configstruc:
            print('Checking {} structure... '.format(p))
            if p in self.config:
                for x in self.config[p]:
                    print(' - {}/{}... '.format(p,x),end='')
                    if not x in self.configstruc[p]:
                        self.missing(self.pred('{}/{} in config.plist'.format(p,x)))
                        self.error.append('Missing {}/{} in config.plist'.format(p,x))
                    print(self.pgreen('OK'))
                    time.sleep(0.1)
            else:
                print(self.pred('Skipped because of missing {}'.format(p)))
                time.sleep(0.1)
        time.sleep(1)
        self.checkacpi()

    def checkacpi(self):
        self.clear()
        self.title('Checking ACPI... ')
        if 'ACPI' in self.config:
            files = os.listdir('./ACPI')
            print('')
            if files != ['.DS_Store','._.DS_Store']:
                print('Checking ACPI/Add...')
                for f in files:
                    if f.endswith('.aml') and not f.startswith('._'):
                        b = False
                        print(' - Checking {}... '.format(f),end='')
                        for item in self.config['ACPI']['Add']:
                            if item['Path'] == f:
                                b = True
                                if 'Enabled' in item:
                                    if item['Enabled'] == False:
                                        print(self.pred('Error'))
                                        print(self.pred('   Enabled is not set to True in ACPI/Add/{}'.format(f)))
                                        self.error.append('Enabled is not set to True in ACPI/Add/{}'.format(f))
                                    else:
                                        print(self.pgreen('OK'))
                                else:
                                    print(self.pred('Error'))
                                    print(self.pred('    Enabled is not set in ACPI/Add/{}'.format(f)))
                                    self.error.append('Enabled is not set in ACPI/Add/{}'.format(f))
                                break
                        if b == False:
                            print(self.pred('Error'))
                            print(self.pred('   Missing {} in ACPI/Add'.format(f)))
                            self.error.append('Missing {} in ACPI/Add'.format(f))
                    time.sleep(0.1)
            else:
                print('Skipping ACPI/Add...')
            time.sleep(0.1)
            print('Checking Quirks...')
            for quirk in self.acpiquirks:
                print(' - Checking ACPI/Quirks/{}... '.format(quirk), end='')
                if quirk in self.config['ACPI']['Quirks']:
                    if self.acpiquirkset[quirk] == self.config['ACPI']['Quirks'][quirk]:
                        print(self.pgreen('OK'))
                    else:
                        print(self.pred('Error'))
                        print(self.pred('   {} should be set to {}'.format(quirk, self.acpiquirkset[quirk])))
                        self.error.append('{} should be set to {}'.format(quirk, self.acpiquirkset[quirk]))
                else:
                    print(self.pred('Error'))
                    print(self.pred('   Missing {} in config.plist'.format(quirk)))
                    self.error.append('Missing {} in config.plist'.format(quirk))
                time.sleep(0.1)
            time.sleep(0.5)
            print(self.pgreen('Done'))
        else:
            print(self.pred('Skipping ACPI part because of missing ACPI in config.plist...'))
            time.sleep(1)

        print(self.pred('All errors: '), end='')
        if self.error != []:
            print('')
            for n in self.error:
                print(self.pred(' - {}'.format(n)))
        else:
            print(self.pgreen('None'))
            
    def main(self):
        # Clear the window first
        self.clear()
        # We need to gather some information first
        self.info()
        

if __name__ == "__main__":
    r = occhecker()
    r.main()