<template>
  <ion-page>
    <ion-content :fullscreen="true">
      <FormView
        v-if="formFields.data"
        doctype="Task"
        v-model="projectTask"
        :isSubmittable="true"
        :fields="formFields.data"
        :id="props.id"
        @validateForm="validateForm"
      />
    </ion-content>
  </ion-page>
</template>

<script setup>
import { IonPage, IonContent } from "@ionic/vue";
import { createResource } from "frappe-ui";
import { ref, inject } from "vue";

import FormView from "@/components/FormView.vue";
const props = defineProps({
  id: {
    type: String,
    required: false,
  },
});

const employee = inject("$employee");

const projectTask = ref({
  task_report: [],
});

const formFields = createResource({
  url: "hrms.api.get_doctype_fields",
  params: { doctype: "Task" },
  auto: true,
  transform(data) {
    const allowedFields = ["date", "subject", "description"];
    return data.filter((field) => allowedFields.includes(field.fieldname));
  },
});

function validateForm() {
  if (!props.id && employee?.data?.name) {
    projectTask.value.employee = employee.data.name;
  }
}
</script>
