import { BACKEND_API } from "./config.ts";

// type DiscordInviteResponse = {
//   invite_link: string;
// };

export async function fetchDiscordInvite() {
  // const res = await fetch(
  //   `${BACKEND_API}/get_discord_invite`,
  // );
  // const data: DiscordInviteResponse = await res.json();
  // return data.invite_link;

  const discordInvite =
    (typeof Deno !== "undefined" && typeof Deno.env?.get === "function"
      ? Deno.env.get("DISCORD_INVITE")
      : undefined) ??
    (typeof process !== "undefined" && process?.env
      ? process.env.DISCORD_INVITE
      : undefined) ??
    (globalThis as any)?.DISCORD_INVITE;

  if (!discordInvite) {
    throw new Error("DISCORD_INVITE environment variable is not defined");
  }

  return discordInvite;
}
