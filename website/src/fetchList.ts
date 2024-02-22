import { BACKEND_API } from "./config.ts";

export type BlockedUser = {
  username: string;
  changed_on: number;
  reason: string;
};

export async function fetchBlockList() {
  const res = await fetch(
    `${BACKEND_API}/get_blocked_users`,
  );
  const data: BlockedUser[] = await res.json();
  return data;
}
