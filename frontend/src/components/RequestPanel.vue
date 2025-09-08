<template>
  <div class="w-full">
    <TabButtons :buttons="TAB_BUTTONS" v-model="activeTab" />
    <RequestList v-if="activeTab == 'My Requests'" :items="myRequests" />
    <RequestList
      v-else-if="activeTab == 'Team Requests'"
      :items="teamRequests"
      :teamRequests="true"
    />
  </div>
</template>

<script setup>
import { ref, inject, onMounted, computed, markRaw } from "vue";

import TabButtons from "@/components/TabButtons.vue";
import RequestList from "@/components/RequestList.vue";
import { getDates } from "@/data/wfh";

import {
  myAttendanceRequests,
  myShiftRequests,
  teamShiftRequests,
} from "@/data/attendance";
import { myClaims, teamClaims } from "@/data/claims";
import { myLeaves, teamLeaves } from "@/data/leaves";
import { myWFH, teamWFH } from "@/data/wfh";
import AttendanceRequestItem from "@/components/AttendanceRequestItem.vue";
import ExpenseClaimItem from "@/components/ExpenseClaimItem.vue";
import LeaveRequestItem from "@/components/LeaveRequestItem.vue";
import ShiftRequestItem from "@/components/ShiftRequestItem.vue";
import WFHRequestItem from "@/components/WFHRequestItem.vue";

import { useListUpdate } from "@/composables/realtime";

const activeTab = ref("My Requests");
const socket = inject("$socket");

const TAB_BUTTONS = ["My Requests", "Team Requests"]; // __("My Requests"), __("Team Requests")

const myRequests = computed(() =>
  updateRequestDetails(myWFH, myLeaves, myClaims, myShiftRequests, myAttendanceRequests)
);

const teamRequests = computed(() =>
  updateRequestDetails(teamWFH, teamLeaves, teamClaims, teamShiftRequests)
);

function updateRequestDetails(wfhs, leaves, claims, shiftRequests, attendanceRequests) {
  const requests = [wfhs, leaves, claims, shiftRequests, attendanceRequests].reduce(
    (acc, resource) => acc.concat(resource?.data || []),
    []
  );

  const componentMap = {
    "Leave Application": LeaveRequestItem,
    "Expense Claim": ExpenseClaimItem,
    "Shift Request": ShiftRequestItem,
    "Attendance Request": AttendanceRequestItem,
    "Work From Home": WFHRequestItem,
  };
  requests.forEach((request) => {
    request.component = markRaw(componentMap[request.doctype]);
  });

  return getSortedRequests(requests);
}

function getSortedRequests(list) {
  // return top 10 requests sorted by posting date
  return list
    .sort((a, b) => {
      return new Date(b.creation) - new Date(a.creation);
    })
    .splice(0, 10);
}

onMounted(() => {
  useListUpdate(socket, "Work From Home", () => teamWFH.reload());
  useListUpdate(socket, "Leave Application", () => teamLeaves.reload());
  useListUpdate(socket, "Expense Claim", () => teamClaims.reload());
});
</script>
