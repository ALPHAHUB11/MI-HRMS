<template>
  <ion-page>
    <ion-content :fullscreen="true">
      <!-- Form Section -->
      <FormView
        v-if="formFields.data"
        doctype="Work From Home"
        v-model="workFromHome"
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

// Inject employee data for current user
const employee = inject("$employee");

// Props for dynamic behavior
const props = defineProps({
  id: {
    type: String,
    required: false,
  },
});

// Reactive state
const workFromHome = ref({});

// Fetch form fields for the Work From Home doctype
const formFields = createResource({
  url: "hrms.api.get_doctype_fields",
  params: { doctype: "Work From Home" },
  auto: true,
  transform(data) {
    if (props.id) return data;
    return data.filter((field) =>
      ["from_date", "to_date", "reason"].includes(field.fieldname)
    );
  },
});

// Form validation function
function validateForm() {
  if (employee?.data?.name) {
    workFromHome.value.employee = employee.data.name; // Set employee name
  }
}
</script>
