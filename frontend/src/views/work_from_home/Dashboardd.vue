<template>
  <BaseLayout :pageTitle="__('Work From Home')">
    <template #body>
      <div class="flex flex-col items-center mt-7 mb-7 py-4">
        <div class="flex flex-col gap-7 mt-5 px-4 w-full">
          <router-link :to="{ name: 'WhfDetails' }" v-slot="{ navigate }">
            <Button @click="navigate" variant="solid" class="py-5 text-base w-full">
              {{ __("Request a Leave") }}
            </Button>
          </router-link>
          <div>
            <div class="text-lg text-gray-800 font-bold">{{ __("Recent Leaves") }}</div>
            <RequestList
              :component="markRaw(WFHRequestItem)"
              :items="myWFH.data"
              :addListButton="true"
              listButtonRoute="WhfDetails"
            />
          </div>
          <Holidays />
        </div>
      </div>
    </template>
  </BaseLayout>
</template>

<script setup>
import { markRaw } from "vue";

import BaseLayout from "@/components/BaseLayout.vue";
import RequestList from "@/components/RequestList.vue";
import WFHRequestItem from "@/components/WFHRequestItem.vue";
import Holidays from "@/components/Holidays.vue";
import { myWFH } from "@/data/wfh";
</script>
