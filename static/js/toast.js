document.addEventListener("DOMContentLoaded", function () {
  const toasts = document.querySelectorAll(".toast");
  toasts.forEach((toast) => {
    let delay = 6000; // Default to 6 seconds if not specified

    if (
        toast.classList.contains("bg-danger") || toast.classList.contains("bg-warning")
    ) 
    {
      bootstrap.Toast.getOrCreateInstance(toast, { autohide: false }).show();
    }
    else {
      bootstrap.Toast.getOrCreateInstance(toast, { delay }).show();
    }
  });
});
