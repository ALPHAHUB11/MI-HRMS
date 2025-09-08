<template>
  <BaseLayout>
    <template #body>
      <div class="flex flex-col items-center my-7 p-4 gap-7">
        <CheckInPanel />
        <QuickLinks :items="filteredQuickLinks" :title="__('Quick Links')" />
        <RequestPanel />
      </div>
    </template>
  </BaseLayout>
</template>

<script setup>
import { inject, markRaw, ref, computed, onMounted } from "vue";
import axios from "axios";

import HomeIcon from "@/components/icons/HomeIcon.vue";
import AllEmpIcon from "@/components/icons/AllEmpIcon.vue";
import CheckInPanel from "@/components/CheckInPanel.vue";
import QuickLinks from "@/components/QuickLinks.vue";
import BaseLayout from "@/components/BaseLayout.vue";
import RequestPanel from "@/components/RequestPanel.vue";
import AttendanceIcon from "@/components/icons/AttendanceIcon.vue";
import ShiftIcon from "@/components/icons/ShiftIcon.vue";
import LeaveIcon from "@/components/icons/LeaveIcon.vue";
import ExpenseIcon from "@/components/icons/ExpenseIcon.vue";
import EmployeeAdvanceIcon from "@/components/icons/EmployeeAdvanceIcon.vue";
import SalaryIcon from "@/components/icons/SalaryIcon.vue";

const __ = inject("$translate");
const employeeInfo = ref({ custom_eligible_for_work_from_home: "No" });

const quickLinks = ref([
  {
    icon: markRaw(AttendanceIcon),
    title: __("Request Attendance"),
    route: "AttendanceRequestFormView",
  },
  {
    icon: markRaw(ShiftIcon),
    title: __("Request a Shift"),
    route: "ShiftRequestFormView",
  },
  {
    icon: markRaw(LeaveIcon),
    title: __("Request Leave"),
    route: "LeaveApplicationFormView",
  },
  {
    icon: markRaw(ExpenseIcon),
    title: __("Claim an Expense"),
    route: "ExpenseClaimFormView",
  },
  {
    icon: markRaw(EmployeeAdvanceIcon),
    title: __("Request an Advance"),
    route: "EmployeeAdvanceFormView",
  },
  {
    icon: markRaw(SalaryIcon),
    title: __("View Salary Slips"),
    route: "SalarySlipsDashboard",
  },
  {
    icon: markRaw(AllEmpIcon),
    title: __("Employee Info"),
    route: "EmployeeInfo",
  },
]);

const fetchEmployeeInfo = async () => {
  try {
    const response = await axios.get("/api/method/hrms.api.get_current_employee_info", {
      headers: { "X-Frappe-CSRF-Token": window.csrf_token || "" },
    });
    employeeInfo.value = response.data.message || {};
  } catch (error) {
    console.error("Error fetching employee info:", error);
  }
};

const filteredQuickLinks = computed(() => {
  if (!employeeInfo.value) return quickLinks.value;

  return employeeInfo.value.custom_eligible_for_work_from_home === "Yes"
    ? [
        ...quickLinks.value,
        {
          icon: markRaw(HomeIcon),
          title: __("Request Work From Home"),
          route: "WorkFromHomeDashboard",
        },
        {
          icon: markRaw(HomeIcon),
          title: __("Work From Home Request History"),
          route: "HistoryView",
        },
      ]
    : quickLinks.value;
});

onMounted(fetchEmployeeInfo);
</script>
