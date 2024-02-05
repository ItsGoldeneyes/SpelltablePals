export type BlockedUser = {
  username: string;
  changed_on: number;
  reason: string;
};

export async function fetchBlockList() {
  const res = await fetch(
    "https://backend-production-c33b.up.railway.app/get_blocked_users",
  );
  const data: BlockedUser[] = await res.json();
  return data;
}
