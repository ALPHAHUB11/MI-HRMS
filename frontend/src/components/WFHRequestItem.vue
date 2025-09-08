<template>
  <ListItem
    :isTeamRequest="props.isTeamRequest"
    :employee="props.doc.employee"
    :employeeName="props.doc.employee_name"
  >
    <template #left>
      <LeaveIcon class="h-5 w-5 text-gray-500 bg-blue-200" />
      <div class="flex flex-col items-start gap-1.5">
        <div class="text-base font-normal text-gray-800">
          {{ __("Work From Home") }}
        </div>
        <div class="text-xs font-normal text-gray-500">
          <span>{{ props.doc.wfh_dates || getDates(props.doc) }}</span>
          <span class="whitespace-pre"> &middot; </span>
        </div>
      </div>
    </template>
    <template #right>
      <Badge
        variant="outline"
        :theme="colorMap[status]"
        :label="__(status, null, 'Work From Home')"
        size="md"
      />
      <FeatherIcon name="chevron-right" class="h-5 w-5 text-gray-500" />
    </template>
  </ListItem>
</template>

<script setup>
import { computed } from "vue";
import { FeatherIcon, Badge } from "frappe-ui";

import ListItem from "@/components/ListItem.vue";
import LeaveIcon from "@/components/icons/LeaveIcon.vue";
import { getDates } from "@/data/wfh";
const props = defineProps({
  doc: {
    type: Object,
  },
  isTeamRequest: {
    type: Boolean,
    default: false,
  },
  workflowStateField: {
    type: String,
    required: false,
  },
});

const status = computed(() => {
  return props.workflowStateField
    ? props.doc[props.workflowStateField]
    : props.doc.status;
});

const colorMap = {
  Approved: "green",
  Rejected: "red",
  Open: "orange",
};
</script>
