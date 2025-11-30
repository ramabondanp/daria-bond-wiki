# Unlock Bootloader Bond 1 (Required for Root and Custom ROMs)

!!! warning "Important Warning"
    Unlocking the bootloader will **erase all data on your phone**.
    Make sure to **backup your important files and data**.

The **Daria Bond 1** phone is very close to stock Android, and unlocking its bootloader is easily done with the following command:

```bash
fastboot flashing unlock
```

But before reaching this step, you need to perform a few preparation steps 👇

---

## Bootloader Unlock Steps

### 1. Enable Developer Options and USB Debugging

1. Go to **Settings**.
2. Navigate to **About phone → Build number**.
3. Tap on *Build number* several times (about 7 times) until the message *"You are now a developer!"* appears.
4. Go to **Settings → System → Developer options**.
5. Enable the following options:

   * **OEM unlocking**
   * **USB debugging**

---

### 2. Install ADB and Fastboot on Computer

To communicate with the phone via USB, you need the **ADB** and **Fastboot** tools.

<details>
<summary>💻 Install Drivers and ADB on Windows</summary>

<a href="https://t.me/dariabond_group/62787">Download and Install Drivers and ADB</a>

</details>

<details>
<summary>🐧 Install ADB on Linux</summary>

<h3>Debian / Ubuntu:</h3>

```bash
sudo apt update
sudo apt install android-tools-adb android-tools-fastboot
```

<h3>Fedora:</h3>

```bash
sudo dnf install android-tools
```

<h3>Arch Linux:</h3>

```bash
sudo pacman -S android-tools
```

After installation, verify with:

```bash
adb version
```

</details>

---

### 3. Reboot to Fastboot Mode

1. Connect the phone to the computer via USB cable.
2. Enter the following command in the terminal:

   ```bash
   adb reboot bootloader
   ```
3. Wait for the phone to enter Fastboot mode (a screen displaying "FASTBOOT MODE").

---

### 4. Unlock Bootloader

Now enter the following command:

```bash
fastboot flashing unlock
```

A confirmation message will appear on the phone. Confirm with the **Volume** keys to start the unlock process.

Once done, the phone will reset and the **bootloader is unlocked** ✅

---

### 5. Reboot to Android

If the phone does not reboot automatically, enter the command:

```bash
fastboot reboot
```

The phone will turn on again, and on the boot screen, you will see a message like *"Bootloader is unlocked"* — meaning you succeeded 🎉

---

### Note:

If you need to re-lock the bootloader (to return to factory state):

```bash
fastboot flashing lock
```

---

📱 Now your phone is ready for **Root, Custom Recovery**, or **Custom ROM**.
