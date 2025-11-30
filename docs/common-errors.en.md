# Common Errors

# kInstallDeviceOpenError
If you see this error while flashing an Android ROM, it is because your phone is on Slot A and that ROM cannot be flashed to the same Slot. Go to the bootloader and enter the following command:
```bash
fastboot set_active b
```
Then go back to recovery and flash the desired ROM.
```bash
fastboot reboot recovery
```
