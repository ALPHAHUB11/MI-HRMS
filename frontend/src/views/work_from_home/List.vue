<template>
  <ion-page>
    <ListView
      doctype="Work From Home"
      :pageTitle="__('Work From Home History')"
      :tabButtons="TAB_BUTTONS"
      :fields="WFH_FIELDS"
      :filterConfig="FILTER_CONFIG"
    />
  </ion-page>
</template>

<script setup>
import { IonPage } from "@ionic/vue";
import ListView from "@/components/ListView.vue";

const TAB_BUTTONS = ["My WFH", "Team WFH"]; // __("My Leaves"), __("Team Leaves")
const WFH_FIELDS = ["name", "from_date", "to_date"];
const STATUS_FILTER_OPTIONS = ["Open", "Approved", "Rejected"];
const FILTER_CONFIG = [
  {
    fieldname: "status",
    fieldtype: "Select",
    label: "Status",
    options: STATUS_FILTER_OPTIONS,
  },
  {
    fieldname: "employee",
    fieldtype: "Link",
    label: "Employee",
    options: "Employee",
  },
  { fieldname: "from_date", fieldtype: "Date", label: "From Date" },
  { fieldname: "to_date", fieldtype: "Date", label: "To Date" },
];
</script>
