from datetime import datetime, timezone
import json
import time
from colorama import Fore
import requests
import random
import string


class tabizoo:
    BASE_URL = "https://api.tabibot.com/api/"
    HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
        "origin": "https://front.tabibot.com",
        "referer": "https://front.tabibot.com/",
        "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24", "Microsoft Edge WebView2";v="131"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    }

    def __init__(self):
        self.query_list = self.load_query("query.txt")
        self.token = None
        self.config = self.load_config()

    def banner(self) -> None:
        """Displays the banner for the bot."""
        self.log("🎉 TabiZoo Free Bot", Fore.CYAN)
        self.log("🚀 Created by LIVEXORDS", Fore.CYAN)
        self.log("📢 Channel: t.me/livexordsscript\n", Fore.CYAN)

    def log(self, message, color=Fore.RESET):
        safe_message = message.encode("utf-8", "backslashreplace").decode("utf-8")
        print(
            Fore.LIGHTBLACK_EX
            + datetime.now().strftime("[%Y:%m:%d ~ %H:%M:%S] |")
            + " "
            + color
            + safe_message
            + Fore.RESET
        )

    def load_config(self) -> dict:
        """
        Loads configuration from config.json.

        Returns:
            dict: Configuration data or an empty dictionary if an error occurs.
        """
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                self.log("✅ Configuration loaded successfully.", Fore.GREEN)
                return config
        except FileNotFoundError:
            self.log("❌ File not found: config.json", Fore.RED)
            return {}
        except json.JSONDecodeError:
            self.log(
                "❌ Failed to parse config.json. Please check the file format.",
                Fore.RED,
            )
            return {}

    def load_query(self, path_file: str = "query.txt") -> list:
        """
        Loads a list of queries from the specified file.

        Args:
            path_file (str): The path to the query file. Defaults to "query.txt".

        Returns:
            list: A list of queries or an empty list if an error occurs.
        """
        self.banner()

        try:
            with open(path_file, "r") as file:
                queries = [line.strip() for line in file if line.strip()]

            if not queries:
                self.log(f"⚠️ Warning: {path_file} is empty.", Fore.YELLOW)

            self.log(f"✅ Loaded {len(queries)} queries from {path_file}.", Fore.GREEN)
            return queries

        except FileNotFoundError:
            self.log(f"❌ File not found: {path_file}", Fore.RED)
            return []
        except Exception as e:
            self.log(f"❌ Unexpected error loading queries: {e}", Fore.RED)
            return []

    def login(self, index: int) -> None:
        self.log("🔒 Attempting to log in...", Fore.GREEN)

        if index >= len(self.query_list):
            self.log("❌ Invalid login index. Please check again.", Fore.RED)
            return

        token = self.query_list[index]
        self.log(
            f"📋 Using token: {token[:10]}... (truncated for security)",
            Fore.CYAN,
        )

        # Ganti header authorization menjadi "rawdata" dengan isinya token
        headers = {**self.HEADERS, "rawdata": token}

        # Endpoint untuk sign-in
        sign_in_url = f"{self.BASE_URL}user/v1/sign-in"
        payload = {"invitation_code": ""}

        try:
            # Lakukan request POST untuk sign-in
            self.log("📡 Sending sign-in request...", Fore.CYAN)
            sign_in_response = requests.post(sign_in_url, headers=headers, json=payload)
            sign_in_response.raise_for_status()
            sign_in_data = sign_in_response.json()

            self.token = token

            # Cek apakah sign-in berhasil
            if (
                sign_in_data.get("code") == 200
                and sign_in_data.get("data", {}).get("is_login") is True
            ):
                self.log("✅ Sign-in successful!", Fore.GREEN)
            else:
                message = sign_in_data.get("message", "Unknown error")
                self.log(f"❌ Sign-in failed: {message}", Fore.RED)
                return

            # Endpoint untuk mendapatkan profile user
            profile_url = f"{self.BASE_URL}user/v1/profile"
            self.log("📡 Fetching user profile...", Fore.CYAN)
            profile_response = requests.get(profile_url, headers=headers)
            profile_response.raise_for_status()
            profile_data = profile_response.json()

            if profile_data.get("code") == 200 and "user" in profile_data.get(
                "data", {}
            ):
                user_info = profile_data["data"]["user"]
                name = user_info.get("name", "Unknown")
                coins = user_info.get("coins", 0)
                level = user_info.get("level", "Unknown")
                create_time = user_info.get("create_time", "Unknown")
                login_time = user_info.get("login_time", "Unknown")

                self.log("✅ Profile fetched successfully!", Fore.GREEN)
                self.log(f"👤 Name: {name}", Fore.LIGHTGREEN_EX)
                self.log(f"💎 Coins: {coins}", Fore.CYAN)
                self.log(f"⭐ Level: {level}", Fore.LIGHTYELLOW_EX)
                self.log(f"⏰ Create Time: {create_time}", Fore.LIGHTMAGENTA_EX)
                self.log(f"⏰ Login Time: {login_time}", Fore.LIGHTMAGENTA_EX)
            else:
                self.log("⚠️ Unexpected profile response structure.", Fore.YELLOW)

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Request failed: {e}", Fore.RED)
            if "sign_in_response" in locals():
                self.log(f"📄 Response content: {sign_in_response.text}", Fore.RED)
        except ValueError as e:
            self.log(f"❌ Data error (JSON decode issue): {e}", Fore.RED)
            if "sign_in_response" in locals():
                self.log(f"📄 Response content: {sign_in_response.text}", Fore.RED)
        except KeyError as e:
            self.log(f"❌ Key error: {e}", Fore.RED)
            if "sign_in_response" in locals():
                self.log(f"📄 Response content: {sign_in_response.text}", Fore.RED)
        except Exception as e:
            self.log(f"❌ Unexpected error: {e}", Fore.RED)
            if "sign_in_response" in locals():
                self.log(f"📄 Response content: {sign_in_response.text}", Fore.RED)

    def task(self) -> None:
        # Nested helper function to normalize the task tag for special quests.
        def normalize_special_task_tag(task_tag: str) -> str:
            if task_tag.endswith("_Special"):
                return task_tag[:-8]  # Remove "_Special" (8 characters)
            if "_task_special_" in task_tag:
                return task_tag.replace("_task_special_", "_")
            return task_tag

        self.log("📡 Fetching task list...", Fore.CYAN)
        headers = {**self.HEADERS, "rawdata": self.token}
        task_list_url = f"{self.BASE_URL}task/v1/list"

        try:
            # Retrieve projects and tasks from task/v1/list
            response = requests.get(task_list_url, headers=headers)
            response.raise_for_status()
            task_list_data = response.json()
            if task_list_data.get("code") != 200:
                self.log("❌ Failed to fetch task list.", Fore.RED)
                return

            projects = task_list_data.get("data", [])
            self.log(
                f"✅ Task list fetched: {len(projects)} projects found.", Fore.GREEN
            )

            # Report Ads: send 3 requests with statuses 3, 2, 1
            for status in [3, 2, 1]:
                ad_id = "".join(
                    random.choices(string.ascii_letters + string.digits, k=5)
                )
                payload_ads = {"status": status, "ad_id": ad_id, "from": "task"}
                self.log(
                    f"📡 Reporting ads (status {status}, ad_id {ad_id})...", Fore.CYAN
                )
                ads_url = f"{self.BASE_URL}ads/v1/report"
                ads_response = requests.post(ads_url, headers=headers, json=payload_ads)
                ads_response.raise_for_status()
                ads_data = ads_response.json()
                if ads_data.get("code") == 200:
                    self.log(f"✅ Ads report success for status {status}.", Fore.GREEN)
                else:
                    self.log(
                        f"❌ Ads report failed for status {status}: {ads_data.get('message')}",
                        Fore.RED,
                    )

            now = datetime.now(timezone.utc)

            # Process each project and its tasks
            for project in projects:
                project_tag = project.get("project_tag", "")
                task_list = project.get("task_list", [])

                for task_item in task_list:
                    task_tag = task_item.get("task_tag", "")
                    user_task_status = task_item.get("user_task_status", 0)

                    # Only process tasks that are not completed (user_task_status == 2)
                    if user_task_status != 2:
                        self.log(
                            f"ℹ️ Task '{task_tag}' already completed (status: {user_task_status}).",
                            Fore.LIGHTGREEN_EX,
                        )
                        continue

                    # Check if the task is active based on its begin and end times
                    task_begin_str = task_item.get("begin_time", "")
                    task_end_str = task_item.get("end_time", "")
                    active = True
                    if (
                        task_begin_str
                        and task_end_str
                        and task_begin_str not in ["", "0001-01-01T00:00:00Z"]
                    ):
                        try:
                            task_begin = datetime.strptime(
                                task_begin_str, "%Y-%m-%dT%H:%M:%SZ"
                            ).replace(tzinfo=timezone.utc)
                            task_end = datetime.strptime(
                                task_end_str, "%Y-%m-%dT%H:%M:%SZ"
                            ).replace(tzinfo=timezone.utc)
                            if now < task_begin or now > task_end:
                                active = False
                        except Exception as e:
                            self.log(
                                f"⚠️ Error parsing time for task '{task_tag}': {e}",
                                Fore.YELLOW,
                            )
                    if not active:
                        self.log(
                            f"ℹ️ Task '{task_tag}' is not active (begin: {task_begin_str}, end: {task_end_str}).",
                            Fore.YELLOW,
                        )
                        continue

                    # If the task belongs to a special project, report it first
                    if project_tag == "task_special":
                        normalized_tag = normalize_special_task_tag(task_tag)
                        payload_report = {"task_tag": normalized_tag}
                        report_url = f"{self.BASE_URL}task/v1/report/go"
                        self.log(
                            f"📡 Reporting special quest for task '{task_tag}' with payload {payload_report}...",
                            Fore.CYAN,
                        )
                        try:
                            report_response = requests.post(
                                report_url, headers=headers, json=payload_report
                            )
                            report_response.raise_for_status()
                            self.log(
                                f"✅ Special report for task '{task_tag}' completed.",
                                Fore.GREEN,
                            )
                        except Exception as e:
                            self.log(
                                f"⚠️ Special report for task '{task_tag}' failed: {e}. Continuing with claim.",
                                Fore.YELLOW,
                            )

                    # Claim the task by calling verify/task endpoint; if error occurs, log and continue
                    try:
                        claim_url = f"{self.BASE_URL}task/v1/verify/task"
                        payload_claim = {"task_tag": task_tag}
                        self.log(f"📡 Claiming task '{task_tag}'...", Fore.CYAN)
                        claim_response = requests.post(
                            claim_url, headers=headers, json=payload_claim
                        )
                        claim_response.raise_for_status()
                        try:
                            claim_data = claim_response.json()
                        except Exception as json_err:
                            self.log(
                                f"⚠️ Failed to decode claim response for task '{task_tag}': {json_err}",
                                Fore.YELLOW,
                            )
                            claim_data = {}
                        if (
                            claim_data.get("code") == 200
                            and claim_data.get("data", {}).get("verify") is True
                        ):
                            reward = claim_data.get("data", {}).get("reward", 0)
                            self.log(
                                f"✅ Task '{task_tag}' claimed successfully! Reward: {reward}",
                                Fore.GREEN,
                            )
                        else:
                            self.log(
                                f"❌ Failed to claim task '{task_tag}': {claim_data.get('message')}",
                                Fore.RED,
                            )
                    except Exception as e:
                        self.log(
                            f"⚠️ Exception during claiming task '{task_tag}': {e}. Continuing with next task.",
                            Fore.YELLOW,
                        )

            # --- Process Extra Tasks from task/v1/project/mine ---
            extra_tasks_url = f"{self.BASE_URL}task/v1/project/mine"
            self.log("📡 Fetching extra tasks...", Fore.CYAN)
            extra_response = requests.get(extra_tasks_url, headers=headers)
            extra_response.raise_for_status()
            extra_data = extra_response.json()
            if extra_data.get("code") == 200:
                extra_projects = extra_data.get("data", [])
                self.log(
                    f"✅ Extra tasks fetched: {len(extra_projects)} projects found.",
                    Fore.GREEN,
                )
                for extra_project in extra_projects:
                    project_tag = extra_project.get("project_tag", "")
                    user_project_status = extra_project.get("user_project_status", 0)
                    if user_project_status != 2:
                        self.log(
                            f"ℹ️ Extra task project '{project_tag}' is not available (status: {user_project_status}).",
                            Fore.LIGHTGREEN_EX,
                        )
                        continue

                    project_begin = extra_project.get("begin_time", "")
                    project_end = extra_project.get("end_time", "")
                    active = True
                    if (
                        project_begin
                        and project_end
                        and project_begin not in ["", "0001-01-01T00:00:00Z"]
                    ):
                        try:
                            begin_dt = datetime.strptime(
                                project_begin, "%Y-%m-%dT%H:%M:%SZ"
                            ).replace(tzinfo=timezone.utc)
                            end_dt = datetime.strptime(
                                project_end, "%Y-%m-%dT%H:%M:%SZ"
                            ).replace(tzinfo=timezone.utc)
                            if now < begin_dt or now > end_dt:
                                active = False
                        except Exception as e:
                            self.log(
                                f"⚠️ Error parsing time for extra project '{project_tag}': {e}",
                                Fore.YELLOW,
                            )
                    if not active:
                        self.log(
                            f"ℹ️ Extra task project '{project_tag}' is not active (begin: {project_begin}, end: {project_end}).",
                            Fore.YELLOW,
                        )
                        continue

                    # For extra tasks, report using a normalized project tag first (ignore response)
                    normalized_tag = normalize_special_task_tag(project_tag)
                    payload_report = {"task_tag": normalized_tag}
                    report_url = f"{self.BASE_URL}task/v1/report/go"
                    self.log(
                        f"📡 Reporting extra task for project '{project_tag}' with payload {payload_report}...",
                        Fore.CYAN,
                    )
                    try:
                        report_response = requests.post(
                            report_url, headers=headers, json=payload_report
                        )
                        report_response.raise_for_status()
                        self.log(
                            f"✅ Extra task report for project '{project_tag}' completed.",
                            Fore.GREEN,
                        )
                    except Exception as e:
                        self.log(
                            f"⚠️ Extra task report for project '{project_tag}' failed: {e}. Continuing with claim.",
                            Fore.YELLOW,
                        )

                    # Claim the extra task using the same verify/task endpoint
                    try:
                        claim_url = f"{self.BASE_URL}task/v1/verify/task"
                        payload_claim = {"task_tag": project_tag}
                        self.log(
                            f"📡 Claiming extra task for project '{project_tag}'...",
                            Fore.CYAN,
                        )
                        claim_response = requests.post(
                            claim_url, headers=headers, json=payload_claim
                        )
                        claim_response.raise_for_status()
                        try:
                            claim_data = claim_response.json()
                        except Exception as json_err:
                            self.log(
                                f"⚠️ Failed to decode claim response for extra project '{project_tag}': {json_err}",
                                Fore.YELLOW,
                            )
                            claim_data = {}
                        if (
                            claim_data.get("code") == 200
                            and claim_data.get("data", {}).get("verify") is True
                        ):
                            reward = claim_data.get("data", {}).get("reward", 0)
                            self.log(
                                f"✅ Extra task for project '{project_tag}' claimed successfully! Reward: {reward}",
                                Fore.GREEN,
                            )
                        else:
                            self.log(
                                f"❌ Failed to claim extra task for project '{project_tag}': {claim_data.get('message')}",
                                Fore.RED,
                            )
                    except Exception as e:
                        self.log(
                            f"⚠️ Exception during claiming extra task for project '{project_tag}': {e}. Continuing with next project.",
                            Fore.YELLOW,
                        )
            else:
                self.log("❌ Failed to fetch extra tasks.", Fore.RED)

        except requests.exceptions.RequestException as e:
            self.log(f"❌ Request error in task function: {e}", Fore.RED)
            self.log(
                f"📄 Response content: {response.text if 'response' in locals() else 'No response'}",
                Fore.RED,
            )
        except Exception as e:
            self.log(f"❌ Unexpected error in task function: {e}", Fore.RED)
            self.log(
                f"📄 Response content: {response.text if 'response' in locals() else 'No response'}",
                Fore.RED,
            )

    def spin(self) -> None:
        self.log("📡 Fetching spin info...", Fore.CYAN)
        headers = {**self.HEADERS, "rawdata": self.token}
        spin_info_url = f"{self.BASE_URL}spin/v1/info"

        try:
            info_response = requests.post(spin_info_url, headers=headers)
            info_response.raise_for_status()
            info_data = info_response.json()
            if info_data.get("code") != 200:
                self.log("❌ Failed to fetch spin info.", Fore.RED)
                return
            energy = info_data["data"]["energy"]["energy"]
            self.log(f"✅ Spin info: Energy available: {energy}", Fore.GREEN)
        except Exception as e:
            self.log(f"❌ Error fetching spin info: {e}", Fore.RED)
            return

        max_multiplier = (
            3  # Maximum multiplier; adjust as needed for efficient energy use.
        )

        # Loop until energy is 0.
        while energy > 0:
            # Use the maximum multiplier possible (if energy < max, use remaining energy)
            multiplier = max_multiplier if energy >= max_multiplier else energy
            payload = {"multiplier": multiplier}
            self.log(f"📡 Playing spin with multiplier {multiplier}...", Fore.CYAN)
            spin_play_url = f"{self.BASE_URL}spin/v1/play"
            try:
                play_response = requests.post(
                    spin_play_url, headers=headers, json=payload
                )
                play_response.raise_for_status()
                play_data = play_response.json()
                if play_data.get("code") != 200:
                    self.log(
                        f"❌ Spin play failed: {play_data.get('message')}", Fore.RED
                    )
                    # You can choose to break or continue; here we break out.
                    break
                # Update energy from the response and extract prize details.
                energy = play_data["data"]["energy"]["energy"]
                prize = play_data["data"].get("prize", {})
                prize_type = prize.get("prize_type", "None")
                prize_amount = prize.get("amount", 0)
                self.log(
                    f"✅ Spin played: Prize: {prize_type} x {prize_amount}. Remaining Energy: {energy}",
                    Fore.GREEN,
                )
            except Exception as e:
                self.log(f"⚠️ Error during spin play: {e}. Continuing...", Fore.YELLOW)
                # Optionally, you could re-fetch spin info here to update 'energy'
                break

        self.log("ℹ️ No energy left for spinning.", Fore.CYAN)

    def levelUp(self) -> None:
        headers = {**self.HEADERS, "rawdata": self.token}
        level_config_url = f"{self.BASE_URL}user/v1/level-config"
        profile_url = f"{self.BASE_URL}user/v1/profile"
        level_up_url = f"{self.BASE_URL}user/v1/level-up"

        try:
            # Fetch level configuration once.
            self.log("📡 Fetching level config...", Fore.CYAN)
            config_response = requests.get(level_config_url, headers=headers)
            config_response.raise_for_status()
            config_data = config_response.json()
            if config_data.get("code") != 200:
                self.log("❌ Failed to fetch level config.", Fore.RED)
                return

            # Expect a list of configuration entries in "data"["user"]
            level_configs = config_data.get("data", {}).get("user", [])
            if not level_configs:
                self.log("❌ No level configuration found.", Fore.RED)
                return

            self.log(
                f"✅ Level config fetched: {len(level_configs)} configurations found.",
                Fore.GREEN,
            )

            # Loop until level up is not possible.
            while True:
                # Fetch current profile.
                self.log("📡 Fetching profile...", Fore.CYAN)
                profile_response = requests.get(profile_url, headers=headers)
                profile_response.raise_for_status()
                profile_data = profile_response.json()
                if profile_data.get("code") != 200:
                    self.log("❌ Failed to fetch profile.", Fore.RED)
                    break

                user_profile = profile_data.get("data", {}).get("user", {})
                coins = user_profile.get("coins", 0)
                current_level = user_profile.get("level", 0)
                current_secondary = user_profile.get("secondary_level", 0)
                self.log(
                    f"✅ Profile: Level {current_level}, Secondary Level {current_secondary}, Coins: {coins}",
                    Fore.GREEN,
                )

                # Find required coins for level up from level_configs.
                required_coins = None
                for config in level_configs:
                    if (
                        config.get("major_level") == current_level
                        and config.get("secondary_level") == current_secondary
                    ):
                        required_coins = config.get("level_up_coin")
                        break

                if required_coins is None:
                    self.log(
                        "❌ Level configuration for current level not found.", Fore.RED
                    )
                    break

                self.log(f"ℹ️ Level up cost: {required_coins} coins.", Fore.CYAN)
                if coins < required_coins:
                    self.log("❌ Not enough coins to level up. Exiting loop.", Fore.RED)
                    break

                # Attempt level up.
                self.log("📡 Attempting level up...", Fore.CYAN)
                level_up_response = requests.post(level_up_url, headers=headers)
                level_up_response.raise_for_status()
                level_up_data = level_up_response.json()
                if level_up_data.get("code") == 200:
                    self.log("✅ Level up successful!", Fore.GREEN)
                else:
                    self.log(
                        f"❌ Level up failed: {level_up_data.get('message')}", Fore.RED
                    )
                    break

        except Exception as e:
            self.log(f"❌ Error in levelUp function: {e}", Fore.RED)

    def draw(self) -> None:
        """
        🎟️ [Auto Draw]
        Automatically draws rewards as long as the user has enough zoo_coins.
        After each draw, it refreshes the profile to update the zoo_coins balance.
        If an error occurs, the process stops immediately.
        Finally, it retrieves the owned materials list and checks crafting availability.
        """
        headers = {**self.HEADERS, "rawdata": self.token}
        profile_url = f"{self.BASE_URL}user/v1/profile"
        draw_url = f"{self.BASE_URL}lottery/v1/draw"
        rewards_url = f"{self.BASE_URL}lottery/v1/owned-rewards"
        crafting_url = f"{self.BASE_URL}synthesis/v1/config"

        while True:
            # Fetch user profile to get zoo_coins balance
            response = requests.get(profile_url, headers=headers)
            if response.status_code != 200:
                self.log(f"⚠️ [Auto Draw] Failed to fetch profile! ({response.status_code})", Fore.RED)
                break

            profile_data = response.json()
            # Menyimpan zoo_coins dari API profile
            zoo_coins = profile_data.get("data", {}).get("user", {}).get("zoo_coins", 0)

            # Check if zoo_coins are sufficient for a draw (misalnya, ambil dari config spin jika perlu)
            if zoo_coins < 20:
                self.log(f"❌ [Auto Draw] Not enough zoo_coins ({zoo_coins}) to draw.", Fore.YELLOW)
                break

            # Perform the draw
            payload = {"draw_type": "free_draw", "draw_times": 1}
            draw_response = requests.post(draw_url, json=payload, headers=headers)

            if draw_response.status_code != 200:
                self.log(f"⚠️ [Auto Draw] Failed to perform draw! ({draw_response.status_code})", Fore.RED)
                break

            draw_data = draw_response.json()
            if draw_data.get("code") != 200:
                self.log(f"⚠️ [Auto Draw] Draw error: {draw_data.get('message')}", Fore.RED)
                break

            # Extract draw result
            basic_materials = draw_data["data"].get("basic_material", [])
            material_info = ", ".join([f"{m['quantity']}x {m['material_name']}" for m in basic_materials]) if basic_materials else "No materials obtained"
            self.log(f"✅ [Auto Draw] Successfully drew: {material_info}!", Fore.GREEN)

            # Update zoo_coins balance locally
            zoo_coins -= draw_data["data"]["cost_zoo"]
            self.log(f"💰 [Auto Draw] Remaining zoo_coins: {zoo_coins}", Fore.CYAN)

            # Stop loop if not enough zoo_coins for another draw
            if zoo_coins < 20:
                self.log("❌ [Auto Draw] Not enough zoo_coins for another draw.", Fore.YELLOW)
                break

        # Fetch owned materials after drawing
        self.get_owned_materials()

        # Fetch crafting recipes and check requirements
        response = requests.get(crafting_url, headers=headers)
        if response.status_code == 200:
            crafting_data = response.json().get("data", {})
            self.check_crafting_requirements(crafting_data)
        else:
            self.log(f"⚠️ [Crafting] Failed to fetch crafting recipes! ({response.status_code})", Fore.RED)


    def check_crafting_requirements(self, recipes: dict) -> None:
        """
        🛠️ [Crafting Check]
        Compares owned materials with crafting requirements.
        """
        materials = self.get_owned_materials(return_data=True)  # Get materials data

        if not materials:
            self.log("⚠️ [Crafting] No materials found, skipping crafting check.", Fore.YELLOW)
            return

        owned_basic = {m["material_id"]: m["quantity"] for m in materials.get("owned_basic_materials", [])}
        # Jika owned_advanced_materials adalah None, kita gunakan list kosong
        owned_advanced = {m["material_id"]: m["quantity"] for m in (materials.get("owned_advanced_materials") or [])}

        for item_name, item in recipes.items():
            requirements = item["requirements"]
            can_craft = True

            for req in requirements:
                material_type = req["type"]
                material_id = req["material_id"]
                required_qty = req["quantity"]

                if material_type == "basic_material":
                    available_qty = owned_basic.get(material_id, 0)
                elif material_type == "advanced_material":
                    available_qty = owned_advanced.get(material_id, 0)
                else:
                    continue  # Skip unknown types

                if available_qty < required_qty:
                    self.log(f"❌ [Crafting] Missing materials for {item_name}: {req['material_name']} ({available_qty}/{required_qty})", Fore.RED)
                    can_craft = False
                    break  # Stop checking this item if any material is missing

            if can_craft:
                self.log(f"✅ [Crafting] You have enough materials to craft {item_name}!", Fore.GREEN)


    def get_owned_materials(self, return_data: bool = False):
        """
        📦 [Owned Materials]
        Retrieves and displays the materials owned by the user.
        """
        headers = {**self.HEADERS, "rawdata": self.token}
        rewards_url = f"{self.BASE_URL}lottery/v1/owned-rewards"
        response = requests.get(rewards_url, headers=headers)

        if response.status_code != 200:
            self.log(f"⚠️ [Owned Materials] Failed to fetch owned materials! ({response.status_code})", Fore.RED)
            return {} if return_data else None

        materials_data = response.json().get("data", {})

        if return_data:
            return materials_data

        basic_materials = materials_data.get("owned_basic_materials", [])
        # Pastikan jika None, kita gunakan list kosong
        advanced_materials = materials_data.get("owned_advanced_materials") or []

        material_list = [f"{m['quantity']}x {m['material_name']}" for m in basic_materials + advanced_materials]
        material_info = ", ".join(material_list) if material_list else "No materials owned."

        self.log(f"📦 [Owned Materials] {material_info}", Fore.BLUE)


    def get_spin_cost_config(self) -> dict:
        """
        🎰 [Spin Cost Config]
        Retrieves the spin cost configuration (free draw times config and basic material config)
        from the lottery profile endpoint.
        """
        headers = {**self.HEADERS, "rawdata": self.token}
        spin_cost_url = f"{self.BASE_URL}lottery/v1/profile"
        response = requests.get(spin_cost_url, headers=headers)

        if response.status_code == 200:
            data = response.json().get("data", {})
            free_draw_times_config = data.get("free_draw_times_config", [])
            basic_material_config = data.get("basic_material_config", [])
            party_tokens_list = data.get("party_tokens_list", [])
            self.log("✅ [Spin Cost] Spin cost configuration fetched successfully.", Fore.GREEN)
            return data
        else:
            self.log(f"⚠️ [Spin Cost] Failed to fetch spin cost configuration! ({response.status_code})", Fore.RED)
            return {}

    def load_proxies(self, filename="proxy.txt"):
        """
        Reads proxies from a file and returns them as a list.

        Args:
            filename (str): The path to the proxy file.

        Returns:
            list: A list of proxy addresses.
        """
        try:
            with open(filename, "r", encoding="utf-8") as file:
                proxies = [line.strip() for line in file if line.strip()]
            if not proxies:
                raise ValueError("Proxy file is empty.")
            return proxies
        except Exception as e:
            self.log(f"❌ Failed to load proxies: {e}", Fore.RED)
            return []

    def set_proxy_session(self, proxies: list) -> requests.Session:
        """
        Creates a requests session with a working proxy from the given list.

        If a chosen proxy fails the connectivity test, it will try another proxy
        until a working one is found. If no proxies work or the list is empty, it
        will return a session with a direct connection.

        Args:
            proxies (list): A list of proxy addresses (e.g., "http://proxy_address:port").

        Returns:
            requests.Session: A session object configured with a working proxy,
                            or a direct connection if none are available.
        """
        # If no proxies are provided, use a direct connection.
        if not proxies:
            self.log("⚠️ No proxies available. Using direct connection.", Fore.YELLOW)
            self.proxy_session = requests.Session()
            return self.proxy_session

        # Copy the list so that we can modify it without affecting the original.
        available_proxies = proxies.copy()

        while available_proxies:
            proxy_url = random.choice(available_proxies)
            self.proxy_session = requests.Session()
            self.proxy_session.proxies = {"http": proxy_url, "https": proxy_url}

            try:
                test_url = "https://httpbin.org/ip"
                response = self.proxy_session.get(test_url, timeout=5)
                response.raise_for_status()
                origin_ip = response.json().get("origin", "Unknown IP")
                self.log(
                    f"✅ Using Proxy: {proxy_url} | Your IP: {origin_ip}", Fore.GREEN
                )
                return self.proxy_session
            except requests.RequestException as e:
                self.log(f"❌ Proxy failed: {proxy_url} | Error: {e}", Fore.RED)
                # Remove the failed proxy and try again.
                available_proxies.remove(proxy_url)

        # If none of the proxies worked, use a direct connection.
        self.log("⚠️ All proxies failed. Using direct connection.", Fore.YELLOW)
        self.proxy_session = requests.Session()
        return self.proxy_session

    def override_requests(self):
        """Override requests functions globally when proxy is enabled."""
        if self.config.get("proxy", False):
            self.log("[CONFIG] 🛡️ Proxy: ✅ Enabled", Fore.YELLOW)
            proxies = self.load_proxies()
            self.set_proxy_session(proxies)

            # Override request methods
            requests.get = self.proxy_session.get
            requests.post = self.proxy_session.post
            requests.put = self.proxy_session.put
            requests.delete = self.proxy_session.delete
        else:
            self.log("[CONFIG] proxy: ❌ Disabled", Fore.RED)
            # Restore original functions if proxy is disabled
            requests.get = self._original_requests["get"]
            requests.post = self._original_requests["post"]
            requests.put = self._original_requests["put"]
            requests.delete = self._original_requests["delete"]


if __name__ == "__main__":
    tabi = tabizoo()
    index = 0
    max_index = len(tabi.query_list)
    config = tabi.load_config()
    if config.get("proxy", False):
        proxies = tabi.load_proxies()

    tabi.log(
        "🎉 [LIVEXORDS] === Welcome to TabiZoo Automation === [LIVEXORDS]", Fore.YELLOW
    )
    tabi.log(f"📂 Loaded {max_index} accounts from query list.", Fore.YELLOW)

    while True:
        current_account = tabi.query_list[index]
        display_account = (
            current_account[:10] + "..."
            if len(current_account) > 10
            else current_account
        )

        tabi.log(
            f"👤 [ACCOUNT] Processing account {index + 1}/{max_index}: {display_account}",
            Fore.YELLOW,
        )

        if config.get("proxy", False):
            tabi.override_requests()
        else:
            tabi.log("[CONFIG] Proxy: ❌ Disabled", Fore.RED)

        tabi.login(index)

        tabi.log("🛠️ Starting task execution...")
        tasks = {
            "task": "🧩 Auto Solve Task: Automatically solve tasks quickly and efficiently.",
            "spin": "🔄 Auto Spin: Spin automatically to earn rewards.",
            "levelUp": "⬆️ Auto Level Up: Automatically level up your skills to boost performance.",
            "draw": "🎟️ Auto Draw: Automatically perform draws as long as zoo_coins are sufficient, then check owned materials and crafting options.",
        }

        for task_key, task_name in tasks.items():
            task_status = config.get(task_key, False)
            tabi.log(
                f"[CONFIG] {task_name}: {'✅ Enabled' if task_status else '❌ Disabled'}",
                Fore.YELLOW if task_status else Fore.RED,
            )

            if task_status:
                tabi.log(f"🔄 Executing {task_name}...")
                getattr(tabi, task_key)()

        if index == max_index - 1:
            tabi.log("🔁 All accounts processed. Restarting loop.")
            tabi.log(
                f"⏳ Sleeping for {config.get('delay_loop', 30)} seconds before restarting."
            )
            time.sleep(config.get("delay_loop", 30))
            index = 0
        else:
            tabi.log(
                f"➡️ Switching to the next account in {config.get('delay_account_switch', 10)} seconds."
            )
            time.sleep(config.get("delay_account_switch", 10))
            index += 1
