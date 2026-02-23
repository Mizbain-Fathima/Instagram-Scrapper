import time

class FailoverExecutor:

    def __init__(self, identity_manager, max_attempts=5):
        self.identity_manager = identity_manager
        self.max_attempts = max_attempts

    def run(self, task_func, url):
        """
        task_func(identity, url) -> result
        """

        last_error = None

        for attempt in range(self.max_attempts):

            identity = self.identity_manager.get_identity()
            print(f"\n🔄 Attempt {attempt+1}/{self.max_attempts} using {identity.name}")

            try:
                result = task_func(identity, url)

                if result:
                    print(f"✅ Success with {identity.name}")
                    return result

            except Exception as e:
                last_error = e
                msg = str(e)

                # network / edge / block errors
                retryable = any(x in msg.lower() for x in [
                    "connectex",
                    "timeout",
                    "blocked",
                    "challenge",
                    "401",
                    "403"
                ])

                if not retryable:
                    print("⛔ Non-retryable error:", e)
                    raise e

                print(f"⚠ Failed on {identity.name} — rotating identity")
                time.sleep(2)

        raise Exception(f"All identities failed: {last_error}")