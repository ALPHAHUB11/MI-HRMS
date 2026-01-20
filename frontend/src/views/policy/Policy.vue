<template>
  <ion-page>
    <ion-content :fullscreen="true">
      <div class="policy-wrapper sm:w-96">
        <h2 class="text-xl font-medium text-black-600 mb-4 text-center">
          Company Policy
        </h2>

        <!-- Divider -->
        <hr class="my-4 border-gray-200" />

        <!-- Policies Section -->
        <div>
          <!-- Loading -->
          <div v-if="loading" class="text-sm text-gray-500">
            Loading policies...
          </div>

          <!-- Error -->
          <div v-else-if="error" class="text-sm text-red-500">
            {{ error }}
          </div>

          <!-- No policies -->
          <div v-else-if="policies.length === 0" class="text-sm text-gray-500">
            No active policies found.
          </div>

          <!-- Policy list -->
          <ul v-else class="space-y-3">
            <li
              v-for="policy in policies"
              :key="policy.name"
              class="p-3 border border-gray-200 rounded-lg bg-gray-50"
            >
              <div class="font-medium text-sm mb-2">
                {{ policy.policy_title || policy.name }}
              </div>

              <!-- View + Download Row -->
              <div class="flex justify-between items-center mt-2">
                <!-- VIEW (LEFT) -->
                <a
                  v-if="policy.policy_document"
                  :href="policy.policy_document"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="text-xs text-blue-600 underline"
                >
                  👁️ View
                </a>


                <p
                  v-else
                  class="text-xs text-gray-500 italic w-full text-center"
                >
                  No document attached.
                </p>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { IonPage, IonContent } from "@ionic/vue";
import { ref, onMounted } from "vue";

const policies = ref([]);
const loading = ref(false);
const error = ref("");

// Fetch active company policies from backend
onMounted(async () => {
  loading.value = true;
  error.value = "";

  try {
    const response = await fetch(
      "/api/method/mohan_impex.company_policy.company_policy"
    );
    const result = await response.json();

    if (result && result.message) {
      policies.value = result.message;
    } else {
      policies.value = [];
    }
  } catch (err) {
    console.error("Failed to load company policies:", err);
    error.value = "Failed to load company policies. Please try again later.";
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
/* Wrapper for consistent page padding like other screens */
.policy-wrapper {
  padding: 1.5rem;
}

/* Heading style */
.text-xl {
  font-size: 1.25rem;
  font-weight: 500;
  color: #374151;
}
</style>
