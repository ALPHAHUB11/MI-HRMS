<template>
  <div class="p-2 space-y-4">
    <ion-button expand="block" v-if="!isReadOnly" @click="openModal()">
      Add Task Report
    </ion-button>

    <ion-card
      v-for="(row, index) in taskReport"
      :key="index"
      class="shadow-md p-3 rounded-lg"
      @click="openModal(row, index)"
    >
      <ion-item>
        <ion-label>
          <h3 class="text-base font-semibold text-gray-900">
            {{ row.report || "Untitled Report" }}
          </h3>
          <p class="text-sm text-gray-500">Duration: {{ row.duration || "-" }}</p>
        </ion-label>
        <ion-icon name="chevron-forward-outline" slot="end"></ion-icon>
      </ion-item>
    </ion-card>

    <EmptyState
      v-if="!taskReport || !taskReport.length"
      message="No task reports added yet"
      :isTableField="true"
    />

    <CustomIonModal :isOpen="isModalOpen" @didDismiss="resetModal()">
      <template #actionSheet>
        <div class="bg-white w-full flex flex-col items-center justify-center pb-5">
          <div class="w-full pt-8 pb-5 border-b text-center">
            <span class="text-gray-900 font-bold text-xl">
              {{ editingIdx === null ? "New Task Report" : "Edit Task Report" }}
            </span>
          </div>

          <div class="w-full flex flex-col gap-5 p-4">
            <ion-item>
              <ion-label position="stacked">Report</ion-label>
              <ion-input
                v-model="taskEntry.report"
                :readonly="isReadOnly"
                placeholder="Enter report"
              />
            </ion-item>

            <ion-item>
              <ion-label position="stacked">Duration</ion-label>
              <ion-input
                v-model="taskEntry.duration"
                :readonly="isReadOnly"
                type="time"
                placeholder="HH:MM"
              />
            </ion-item>

            <div
              v-if="!isReadOnly"
              class="flex flex-row items-center justify-between w-full"
            >
              <Button
                v-if="editingIdx !== null"
                variant="outline"
                theme="red"
                customClass="text-red-600 border-red-600 w-1/3"
                @click="deleteEntry"
              >
                <template #prefix>
                  <FeatherIcon name="trash" class="w-4" />
                </template>
                Delete
              </Button>

              <Button
                variant="solid"
                customClass="w-full"
                :disabled="!taskEntry.report || !taskEntry.duration"
                @click="saveEntry"
              >
                <template #prefix>
                  <FeatherIcon
                    :name="editingIdx === null ? 'plus' : 'check'"
                    class="w-4"
                  />
                </template>
                {{ editingIdx === null ? "Add Report" : "Update Report" }}
              </Button>
            </div>
          </div>
        </div>
      </template>
    </CustomIonModal>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { IonButton, IonInput, IonItem, IonLabel, IonCard, IonIcon } from "@ionic/vue";
import { FeatherIcon } from "frappe-ui";

import Button from "@/components/Button.vue";
import EmptyState from "@/components/EmptyState.vue";
import CustomIonModal from "@/components/CustomIonModal.vue";

const props = defineProps({
  taskReport: {
    type: Array,
    required: true,
  },
  isReadOnly: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["addReportRow", "updateReportRow", "deleteReportRow"]);

const isModalOpen = ref(false);
const taskEntry = ref({});
const editingIdx = ref(null);

function openModal(row = null, index = null) {
  taskEntry.value = row ? { ...row } : { report: "", duration: "" };
  editingIdx.value = index;
  isModalOpen.value = true;
}

function resetModal() {
  isModalOpen.value = false;
  taskEntry.value = {};
  editingIdx.value = null;
}

function saveEntry() {
  if (editingIdx.value === null) {
    emit("addReportRow", { ...taskEntry.value });
  } else {
    emit("updateReportRow", { ...taskEntry.value }, editingIdx.value);
  }
  resetModal();
}

function deleteEntry() {
  emit("deleteReportRow", editingIdx.value);
  resetModal();
}
</script>
