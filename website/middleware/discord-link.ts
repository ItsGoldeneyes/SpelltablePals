import { FreshContext } from "$fresh/server.ts";
import { fetchDiscordInvite } from "../src/mod.ts";

export async function DiscordLinkMiddleware(
  req: Request,
  ctx: FreshContext,
) {
  const url = new URL(req.url);
  const path = url.pathname;
  if (path === "/discord") {
    const invite = await fetchDiscordInvite();
    if (invite === "None") {
      return new Response(
        "Our Discord is currently not taking any more invites, sorry",
        { status: 403 },
      );
    }
    return Response.redirect(invite, 307);
  }
  return ctx.next();
}
