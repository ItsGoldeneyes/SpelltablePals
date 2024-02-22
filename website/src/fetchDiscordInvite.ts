import { BACKEND_API } from "./config.ts";

type DiscordInviteResponse = {
  invite_link: string;
};

export async function fetchDiscordInvite() {
  const res = await fetch(
    `${BACKEND_API}/get_discord_invite`,
  );
  const data: DiscordInviteResponse = await res.json();
  return data.invite_link;
}
