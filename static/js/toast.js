document.addEventListener("DOMContentLoaded", function () {
  const toasts = document.querySelectorAll(".toast");
  toasts.forEach((toast) => {
    let delay = 2000; // Default to 2 seconds if not specified

    if (
        toast.classList.contains("bg-danger") || toast.classList.contains("bg-warning")
    ) 
    {
      bootstrap.Toast.getOrCreateInstance(toast, { autohide: false }).show();
    } else if (
        toast.classList.contains("bg-info")
    ) {
      bootstrap.Toast.getOrCreateInstance(toast, { delay : 6000 }).show();
    }
    else {
      bootstrap.Toast.getOrCreateInstance(toast, { delay }).show();
    }
  });
});
