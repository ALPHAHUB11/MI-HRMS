<template>
   <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    viewBox="0 0 24 24"
    fill="blue"
  >
    <!-- Background employee (smaller, shifted left) -->
    <g transform="translate(-4,0) scale(0.8)">
      <circle cx="12" cy="8" r="4" />
      <path d="M4 22c0-4 4-7 8-7s8 3 8 7H4z" />
    </g>
    <!-- Foreground employee (full size, shifted right) -->
    <g transform="translate(4,0)">
      <circle cx="12" cy="8" r="4" />
      <path d="M4 22c0-4 4-7 8-7s8 3 8 7H4z" />
    </g>
  </svg>
</template>
