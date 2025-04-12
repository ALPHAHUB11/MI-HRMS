<template>
  <ion-page>
    <ion-content :fullscreen="true">
      <div class="employee-list sm:w-96 shadow-2xl">
        <h2 class="text-xl font-medium text-black-600 text-center mb-4">
          All Employee List
        </h2>

        <!-- Search Input -->
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search Employee Name or Contact Heading..."
          class="w-full p-2 mb-4 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <!-- Loading State -->
        <div v-if="loading" class="text-center text-blue-500">Loading employees...</div>

        <!-- Error Message -->
        <div v-else-if="error" class="text-red-500 text-center">{{ error }}</div>

        <!-- No Records Found -->
        <div
          v-else-if="filteredEmployees.length === 0"
          class="text-red-500 text-center text-sm"
        >
          No employee records found.
        </div>

        <!-- Employee Table -->
        <div v-else class="overflow-auto">
          <table
            class="employee-table w-full text-left border-collapse border border-gray-300 rounded-lg"
          >
            <thead class="bg-gray-200">
              <tr>
                <th class="py-3 px-4 border border-gray-300">Employee Name</th>
                <th class="py-3 px-4 border border-gray-300">Email</th>
                <th class="py-3 px-4 border border-gray-300">Phone No.</th>
                <th class="py-3 px-4 border border-gray-300">Department</th>
                <th class="py-3 px-4 border border-gray-300">Contact Card Heading</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="employee in filteredEmployees"
                :key="employee.id"
                :class="[
                  'odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors',
                ]"
              >
                <td class="py-3 px-4 border border-gray-300">
                  {{ employee.employee_name }}
                </td>
                <td class="py-3 px-4 border border-gray-300">
                  <a
                    :href="`mailto:${employee.company_email}`"
                    class="text-blue-600 hover:underline"
                  >
                    {{ employee.company_email }}
                  </a>
                </td>
                <td class="py-3 px-4 border border-gray-300">
                  <a
                    :href="`tel:${employee.cell_number}`"
                    class="text-blue-600 hover:underline"
                  >
                    {{ employee.cell_number }}
                  </a>
                </td>
                <td class="py-3 px-4 border border-gray-300">
                  {{ employee.department ? employee.department.slice(0, -9) : "" }}
                </td>
                <td class="py-3 px-4 border border-gray-300">
                  {{ employee.custom_contact_card_heading }}
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
import { ref, computed, onMounted } from "vue";

// Reactive state
const employees = ref([]);
const searchQuery = ref("");
const loading = ref(true);
const error = ref("");

// Computed: filter and sort by employee name
const filteredEmployees = computed(() => {
  const query = searchQuery.value.toLowerCase();
  return employees.value
    .filter((employee) => {
      const name = employee.employee_name?.toLowerCase() || "";
      const heading = employee.custom_contact_card_heading?.toLowerCase() || "";
      return name.includes(query) || heading.includes(query);
    })
    .sort((a, b) => {
      const nameA = a.employee_name?.toLowerCase() || "";
      const nameB = b.employee_name?.toLowerCase() || "";
      return nameA.localeCompare(nameB);
    });
});

// Fetch employee data
onMounted(async () => {
  try {
    const response = await fetch(`/api/method/hrms.api.get_all_employees`);
    const result = await response.json();
    if (result?.message) {
      employees.value = result.message;
    } else {
      error.value = "No employee data available.";
    }
  } catch (err) {
    error.value = "Failed to fetch employee data.";
    console.error("Error fetching employee data:", err);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.employee-list {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
}

.employee-table {
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
</style>
