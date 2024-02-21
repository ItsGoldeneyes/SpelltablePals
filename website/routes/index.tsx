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
    <div class="min-w-[60%] max-w-[80%] m-auto pb-10">
      <div class="flex children:mx-3 m-auto justify-center py-10 pb-0">
        <img
          src="/pals.png"
          alt="Spelltable Pals"
          class="w-24 h-24 rounded-md"
        />
        <div class="children:text-left">
          <h1 class="font-bold text-6xl">Spelltable Pals</h1>
          <h2 class="text-3xl italic">Caution List</h2>
        </div>
      </div>
      <div class="m-auto p-4 w-[50%]">
        <p>
          This is a list of users who the Spelltable Pals have had a poor
          experience with. If you are a member of the Spelltable Pals, please
          use this list to help avoid playing with these users. If you are a
          user on this list, please reach out to the Spelltable Pals to discuss
          the situation and potentially be removed from this list.
        </p>
      </div>
      <div class="flex-row justify-center items-center">
        <BlockListTable
          blocked_users={blockedUsers}
          class="m-auto children:(children:(first:(bg-[rgba(0,0,0,0.5)] text-white) even:(bg-[rgba(0,0,0,0.2)]) p-3) border border-gray-300)"
        />
      </div>
    </div>
  );
}
