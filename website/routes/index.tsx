import { BlockedUser } from "../src/mod.ts";
import { Handlers, PageProps } from "$fresh/server.ts";
import { fetchBlockList } from "../src/mod.ts";
import BlockListTable from "../components/BlockListTable.tsx";

export const handler: Handlers<BlockedUser[]> = {
  GET: async (_req, ctx) => {
    const blockedUsers = await fetchBlockList();
    return ctx.render(blockedUsers);
  },
};

export default function Home(props: PageProps<BlockedUser[]>) {
  const blockedUsers = props.data;
  return (
    <html>
      <body class="min-w-[60%] max-w-[80%] m-auto">
        <div class="flex children:mx-3 m-auto justify-center py-10 pb-0">
          <img
            src="/pals.png"
            alt="Spelltable Pals"
            class="w-24 h-24 rounded-md"
          />
          <div class="children:text-left">
            <h1 class="font-bold text-6xl">Spelltable Pals</h1>
            <h2 class="text-3xl italic">no no list</h2>
          </div>
        </div>
        <div class="flex-row justify-center items-center">
          <div class="m-auto p-4 w-[50%]">
            <p>
              These people have been deemed by the Spelltable Pals community to
              be unworthy of being pals. They have been blocked by the
              community. If you believe you have been blocked in error, please
              contact the Spelltable Pals team.
            </p>
          </div>

          <BlockListTable
            blocked_users={blockedUsers}
            class="m-auto children:(children:(first:(bg-black text-white) even:(bg-gray-200) p-3) border border-gray-300)"
          />
        </div>
      </body>
    </html>
  );
}
