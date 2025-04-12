<template>
  <ion-page>
    <ion-content class="ion-padding">
      <div class="flex flex-col h-screen w-screen">
        <div class="w-full sm:w-96">
          <header
            class="flex flex-row bg-white shadow-sm py-4 px-3 items-center justify-between border-b sticky top-0 z-10"
          >
            <div class="flex flex-row items-center">
              <Button variant="ghost" class="!pl-0 hover:bg-white" @click="router.back()">
                <FeatherIcon name="chevron-left" class="h-5 w-5" />
              </Button>
              <h2 class="text-xl font-semibold text-gray-900">{{ __("Profile") }}</h2>
            </div>
          </header>

          <div class="flex flex-col items-center mt-5 p-4">
            <label for="file-upload" class="relative cursor-pointer">
              <div class="relative">
                <img
                  v-if="user.data.user_image"
                  class="h-24 w-24 rounded-full object-cover border border-gray-300"
                  :src="updatedImage"
                  :alt="user.data.first_name"
                />
                <div
                  v-else
                  class="flex items-center justify-center bg-gray-200 uppercase text-gray-600 h-24 w-24 rounded-full"
                >
                  {{ user.data.first_name[0] }}
                </div>
                <div
                  class="absolute bottom-0 right-0 bg-gray-800 text-white p-1 rounded-full"
                >
                  <FeatherIcon name="camera" class="h-4 w-4" />
                </div>
              </div>
              <input
                type="file"
                id="file-upload"
                ref="fileInput"
                accept="image/*"
                class="hidden"
                @change="handleFileUpload"
              />
            </label>

            <div class="flex flex-col gap-1.5 items-center mt-2 mb-5">
              <span v-if="employee" class="text-lg font-bold text-gray-900">
                {{ employee?.data?.employee_name }}
              </span>
              <span v-if="employee" class="font-normal text-sm text-gray-500">
                {{ employee?.data?.designation }}
              </span>
            </div>

            <Button
              @click="logout"
              variant="outline"
              theme="red"
              class="w-full shadow py-4 mt-5"
            >
              <template #prefix>
                <FeatherIcon name="log-out" class="w-4" />
              </template>
              {{ __("Log Out") }}
            </Button>
          </div>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { ref, computed, inject, nextTick } from "vue";
import { useRouter } from "vue-router";
import { FeatherIcon } from "frappe-ui";
import { IonPage, IonContent } from "@ionic/vue";
import { showErrorAlert } from "@/utils/dialogs";

// Inject dependencies
const router = useRouter();
const user = inject("$user");
const session = inject("$session");
const employee = inject("$employee");
const __ = inject("$translate");

// File input reference
const fileInput = ref(null);

// ✅ Computed property to force image refresh and avoid caching
const updatedImage = computed(() => {
  return user.data.user_image ? `${user.data.user_image}?t=${Date.now()}` : "";
});

// ✅ Function to Fetch CSRF Token from Custom API
const fetchCSRFToken = async () => {
  try {
    const response = await fetch("/api/method/hrms.hrms.csrf_token.get_csrf_token", {
      method: "GET",
      credentials: "include",
    });

    const result = await response.json();
    if (result && result.csrf_token) {
      return result.csrf_token;
    } else {
      console.error("Failed to retrieve CSRF token");
      return null;
    }
  } catch (error) {
    console.error("Error fetching CSRF token:", error);
    return null;
  }
};

// ✅ Function to Handle File Upload
const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) {
    showErrorAlert("No file selected");
    return;
  }

  const csrfToken = await fetchCSRFToken();
  if (!csrfToken) {
    showErrorAlert("Failed to get CSRF token");
    return;
  }

  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = async () => {
    try {
      const response = await fetch("/api/method/hrms.user.update_user_image", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Frappe-CSRF-Token": csrfToken,
        },
        credentials: "include",
        body: JSON.stringify({
          image: reader.result,
          filename: file.name,
        }),
      });

      const result = await response.json();
      console.log("API Response:", result);

      if (result.status === "success") {
        user.data.user_image = result.image_url;
        await nextTick();
      } else {
        showErrorAlert("Upload failed: " + (result.message || "Unknown error"));
      }
    } catch (error) {
      showErrorAlert("Error uploading image: " + error.message);
      console.error("Upload error:", error);
    }
  };
};

// ✅ Function to Log Out User
const logout = async () => {
  try {
    await session.logout.submit();
    router.push("/login");
  } catch (e) {
    showErrorAlert("An error occurred while attempting to log out!");
  }
};
</script>
