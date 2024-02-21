import { FreshContext } from "$fresh/server.ts";
import { tldts } from "../deps.ts";

const invite = "https://discord.com/invite/9QwzXz5Rt5";
const disabled = false;

// TODO(ybabts): Integrate these controls into the database or Discord bot and move this to a separate file

export function handler(
  req: Request,
  ctx: FreshContext,
) {
  const domain = tldts.parse(req.url);
  console.log(domain);
  if (domain.subdomain === "discord") {
    if (disabled) {
      return new Response(
        "Our Discord is currently not taking any more invites, sorry",
        { status: 403 },
      );
    }
    return Response.redirect(invite, 307);
  }
  return ctx.next();
}
