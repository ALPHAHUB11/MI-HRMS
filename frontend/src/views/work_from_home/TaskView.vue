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
        :readOnly="isReadOnly"
        @submit="submitForm"
      />
    </ion-content>
  </ion-page>
</template>

<script setup>
import { IonPage, IonContent } from "@ionic/vue";
import { createResource } from "frappe-ui";
import { ref, watch, inject, onMounted } from "vue";
import FormView from "@/components/FormView.vue";

const employee = inject("$employee");

const props = defineProps({
  id: {
    type: String,
    required: false,
  },
});

const projectTask = ref({});
const isReadOnly = ref(false); // State to manage read-only mode

watch(
  () => projectTask.value.custom_employee,
  (employee_id) => {
    if (props.id && employee_id !== custom_employee.data.name) {
      setFormReadOnly();
    }
  }
);

function setFormReadOnly() {
  isReadOnly.value = true; // Set the form to read-only mode
}

const formFields = createResource({
  url: "hrms.api.get_doctype_fields",
  params: { doctype: "Task" },
  auto: true,
  transform(data) {
    if (props.id) return data;
    return data.filter((field) =>
      ["employee", "project", "subject", "description", "status"].includes(
        field.fieldname
      )
    );
  },
});

function submitForm(task) {
  console.log("Form submitted:", task);
  // Add form submission logic here
}
</script>
