<template>
  <ion-page>
    <!-- ListView for displaying history -->
    <ion-content :fullscreen="true">
      <!-- History Section -->
      <div class="wfh-history sm:w-96 shadow-2xl">
        <h2 class="text-xl font-medium text-black-600 mb-4">
          Work From Home Request History
        </h2>
        <div>
          <div
            v-if="formattedHistory.length === 0"
            class="text-red-500 text-center text-sm"
          >
            No Work From Home history found.
          </div>
          <table
            v-else
            class="history-table w-full text-left border-collapse border border-gray-300 rounded-lg"
          >
            <thead class="bg-gray-200">
              <tr>
                <th class="py-3 px-4 border border-gray-300">From Date</th>
                <th class="py-3 px-4 border border-gray-300">To Date</th>
                <th class="py-3 px-4 border border-gray-300">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="request in formattedHistory"
                :key="request.name"
                class="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors"
              >
                <td class="py-3 px-4 border border-gray-300">
                  {{ request.from_date }}
                </td>
                <td class="py-3 px-4 border border-gray-300">
                  {{ request.to_date }}
                </td>
                <td
                  class="py-3 px-4 border border-gray-300 cursor-pointer text-center"
                  :style="{
                    color: request.status === 'Approved' ? 'green' : 'red',
                    textDecoration:
                      request.status === 'Rejected' ? 'line-through' : 'none',
                  }"
                  @click="redirectToPath(request.status)"
                  :class="
                    request.status === 'Approved'
                      ? 'hover:bg-green-100 hover:text-green-700'
                      : ''
                  "
                >
                  {{ request.status }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { IonPage, IonContent } from "@ionic/vue";
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router"; // Import Vue Router

// Router instance
const router = useRouter();

// Reactive state
const history = ref([]);

// Fetch Work From Home history on mount
onMounted(async () => {
  try {
    const response = await fetch(
      `/api/method/hrms.api.get_wfh_history?employee=EMPLOYEE_ID` // Replace EMPLOYEE_ID dynamically
    );
    const result = await response.json();
    if (result?.message) {
      history.value = result.message;
    }
  } catch (error) {
    console.error("Failed to fetch Work From Home history:", error);
  }
});

// Computed property to format and sort history
const formattedHistory = computed(() => {
  return history.value
    .slice()
    .sort((a, b) => new Date(b.from_date) - new Date(a.from_date))
    .map((request) => ({
      ...request,
      from_date: formatDate(request.from_date),
      to_date: formatDate(request.to_date),
    }));
});

// Helper function to format dates
function formatDate(dateString) {
  if (!dateString) return "";
  const date = new Date(dateString);
  const day = String(date.getDate()).padStart(2, "0");
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const year = date.getFullYear();
  return `${day}-${month}-${year}`;
}

// Redirect function
function redirectToPath(status) {
  console.log("Redirect triggered, status:", status);
  if (status === "Approved") {
    try {
      router.push({ path: "/task" });
    } catch (error) {
      console.error("Redirection failed:", error);
    }
  }
}
</script>

<style scoped>
.wfh-history {
  background: white;
  padding: 1.5rem;
}
.history-table {
  width: 100%;
  overflow-x: auto;
  border-spacing: 0;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 20px;
}
.text-xl {
  font-size: 1.25rem;
  font-weight: 500;
  color: #374151;
}
.hover-bg-green-100:hover {
  background-color: #f0fdf4;
}
.hover-text-green-700:hover {
  color: #065f46;
}
body {
  height: 100%;
  margin: 0;
  font-family: Arial, sans-serif;
}
</style>
