---

<h1 align="center">TabiZoo Bot</h1>

<p align="center">Automate tasks in TabiZoo to enhance your efficiency and maximize your results!</p>

---

## 🚀 **About the Bot**

TabiZoo Bot is designed to automate various tasks in **TabiZoo**, including:

- **Auto Task:** Automatically complete tasks quickly and efficiently.
- **Auto Spin:** Spin automatically to collect rewards.
- **Auto Level Up:** Level up automatically to boost your performance.
- **Auto Draw:** Perform draws automatically as long as you have sufficient zoo_coins.
- **Crafting Check:** Check your owned materials to see if you have enough for crafting (currently, the system only checks and does not perform crafting).

In addition, it provides configurable options such as:

- **Proxy Configuration:** (Optional) Enable proxy support if needed.
- **Custom Delay Settings:** Adjust the loop delay and account switching interval.

With TabiZoo Bot, you can save time and achieve better outcomes with minimal manual intervention.

---

## 🌟 Version v1.1.0

### Updates

- **New Features Added:**
  - **Auto Draw:** Automatically perform draws based on your zoo_coins balance.
  - **Crafting Check:** Verify if you have the necessary materials to craft items (currently check-only, crafting functionality coming in the next update).
- **What's Next:**  
  The upcoming update will introduce a mining system and enable full crafting capabilities.

---

### **Features in This Version:**

```json
{
  "levelUp": true,
  "spin": true,
  "task": true,
  "draw": true,
  "proxy": false,
  "delay_loop": 3000,
  "delay_account_switch": 10
}
```

- **Auto Task:** Automatically solve tasks with speed and precision.
- **Auto Spin:** Spin for rewards automatically to maximize your benefits.
- **Auto Level Up:** Level up automatically to enhance your capabilities.
- **Auto Draw:** Draw rewards automatically as long as zoo_coins are sufficient.
- **Crafting Check:** Check owned materials to determine if crafting is possible (actual crafting will be added later).
- **Proxy Support:** Optional proxy configuration (disabled by default).
- **Delay Settings:** Customize delays for loop intervals (in milliseconds) and account switching (in seconds).

---

## ⚙️ **Configuration in `config.json`**

| **Parameter**          | **Description**                              | **Default** |
| ---------------------- | -------------------------------------------- | ----------- |
| `task`                 | Automate task completion                     | `true`      |
| `spin`                 | Automate reward spins                        | `true`      |
| `levelUp`              | Automate leveling up                         | `true`      |
| `draw`                 | Automate draws based on zoo_coins balance    | `true`      |
| `proxy`                | Enable/Disable proxy usage                   | `false`     |
| `delay_loop`           | Delay before the next loop (in milliseconds) | `3000`      |
| `delay_account_switch` | Delay between account switches (seconds)     | `10`        |

---

## 📥 **How to Register**

Start using TabiZoo Bot by registering through the following link:

<div align="center">
  <a href="https://t.me/tabizoobot/tabizoo?startapp=tabizoo_tg_5438209644" target="_blank">
    <img src="https://img.shields.io/static/v1?message=TabiZoo&logo=telegram&label=&color=2CA5E0&logoColor=white&labelColor=&style=for-the-badge" height="25" alt="telegram logo" />
  </a>
</div>

---

## 📖 **Installation Steps**

1. **Clone the Repository**  
   Copy the project to your local machine:

   ```bash
   git clone https://github.com/livexords-nw/tabiZoo-Bot.git
   ```

2. **Navigate to the Project Folder**  
   Move to the project directory:

   ```bash
   cd tabiZoo-Bot
   ```

3. **Install Dependencies**  
   Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Query**  
   Create a `query.txt` file and add your TabiZoo query data.

5. **Set Up Proxy (Optional)**  
   To use a proxy, create a `proxy.txt` file and add proxies in the format:

   ```
   http://username:password@ip:port
   ```

   - Only HTTP and HTTPS proxies are supported.

6. **Run the Bot**  
   Execute the bot using the following command:
   ```bash
   python main.py
   ```

---

## 🛠️ **Contributing**

This project is developed by **Livexords**. If you have suggestions, questions, or would like to contribute, feel free to contact us:

<div align="center">
  <a href="https://t.me/livexordsscript" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Livexords&logo=telegram&label=&color=2CA5E0&logoColor=white&labelColor=&style=for-the-badge" height="25" alt="telegram logo" />
  </a>
</div>

---
