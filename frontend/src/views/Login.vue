<template>
  <ion-page>
    <ion-content class="ion-padding">
      <div class="flex h-screen w-screen flex-col justify-center bg-white">
        <div class="flex flex-col mx-auto gap-3 items-center">
          <img
            src="https://mohanimpex.co.in/cdn/shop/files/Mohan_Impex_Social_Share_7816798d-6c1c-4152-9ec1-97df3f1de72e.png?crop=center&height=1200&v=1727762826&width=1200"
            alt="Mohan Impex Logo"
            class="h-20 w-auto object-contain"
          />
          <div class="text-3xl font-semibold text-gray-900 text-center">
            {{ __("Login to Mohan Impex") }}
          </div>
        </div>

        <div class="mx-auto mt-10 w-full px-8 sm:w-96">
          <form class="flex flex-col space-y-4" @submit.prevent="submit">
            <Input
              :label="__('Email')"
              placeholder="johndoe@mail.com"
              v-model="email"
              type="text"
              autocomplete="username"
            />
            <div class="relative">
              <Input
                :label="__('Password')"
                :type="passwordVisible ? 'text' : 'password'"
                placeholder="••••••"
                v-model="password"
                autocomplete="current-password"
              />

              <button
                type="button"
                class="absolute right-3 top-7 text-gray-500"
                @click="togglePasswordVisibility"
              >
                <svg
                  v-if="passwordVisible"
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.542-7a9.963 9.963 0 012.292-3.951M6.17 6.17A9.961 9.961 0 0112 5c4.478 0 8.268 2.943 9.542 7a9.963 9.963 0 01-3.384 4.917M9.88 9.88A3 3 0 1114.12 14.12M3 3l18 18"
                  />
                </svg>
                <svg
                  v-else
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-.387 1.155-.987 2.184-1.75 3.05A8.932 8.932 0 0112 19c-4.478 0-8.268-2.943-9.542-7z"
                  />
                </svg>
              </button>
            </div>
            <ErrorMessage :message="errorMessage" />
            <Button
              :loading="session.login.loading"
              variant="solid"
              class="disabled:bg-gray-700 disabled:text-white !mt-6"
            >
              {{ __("Login") }}
            </Button>

            <!-- Forgot Password Button -->
            <!-- <Button
              variant="outline"
              class="text-blue-600 border-blue-600 hover:bg-blue-50 !mt-2"
              @click="redirectToForgotPassword"
            >
              {{ __("Forgot Password?") }}
            </Button> -->
          </form>
          <Button
            variant="outline"
            class="text-blue-600 border-blue-600 hover:bg-blue-50 !mt-2"
            @click="redirectToForgotPassword"
          >
            {{ __("Forgot Password?") }}
          </Button>
          <template v-if="authProviders.data?.length">
            <div class="text-center text-sm text-gray-600 my-4">or</div>
            <div class="space-y-4">
              <a
                v-for="provider in authProviders.data"
                :key="provider.name"
                class="flex items-center justify-center gap-2 transition-colors focus:outline-none text-gray-800 bg-gray-100 hover:bg-gray-200 active:bg-gray-300 focus-visible:ring focus-visible:ring-gray-400 h-7 text-base p-2 rounded"
                :href="provider.auth_url"
              >
                <img class="h-4 w-4" :src="provider.icon" :alt="provider.provider_name" />
                <span>Login with {{ provider.provider_name }}</span>
              </a>
            </div>
          </template>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { IonPage, IonContent } from "@ionic/vue";
import { inject, reactive, ref } from "vue";
import { Input, Button, ErrorMessage, createResource } from "frappe-ui";

const email = ref(null);
const password = ref(null);
const errorMessage = ref("");

const resetPassword = reactive({
  showDialog: false,
  link: "",
});
const otp = reactive({
  showDialog: false,
  tmp_id: "",
  code: "",
  verification: {},
});

const session = inject("$session");

// Reactive state for toggling password visibility
const passwordVisible = ref(false);

function togglePasswordVisibility() {
  passwordVisible.value = !passwordVisible.value;
}

// Redirect function for Forgot Password
function redirectToForgotPassword() {
  window.location.href = "https://erp.mohanimpex.com/#forgot";
}

async function submit() {
  try {
    let response;
    if (otp.showDialog) {
      response = await session.otp(otp.tmp_id, otp.code);
    } else {
      response = await session.login(email.value, password.value);
    }

    if (response.message === "Password Reset") {
      resetPassword.showDialog = true;
      resetPassword.link = response.redirect_to;
    } else {
      resetPassword.showDialog = false;
      resetPassword.link = "";
    }

    // OTP verification
    if (response.verification) {
      if (response.verification.setup) {
        otp.showDialog = true;
        otp.tmp_id = response.tmp_id;
        otp.verification = response.verification;
      } else {
        window.open(
          "/login?redirect-to=" + encodeURIComponent(window.location.pathname),
          "_blank"
        );
      }
    }
  } catch (error) {
    errorMessage.value = error.messages.join("\n");
  }
}

const authProviders = createResource({
  url: "hrms.api.oauth.oauth_providers",
  auto: true,
});
</script>
