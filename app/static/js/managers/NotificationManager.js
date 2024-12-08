class NotificationManager {
    constructor(domManager) {
        this.domManager = domManager;
    }

    updateNotifications() {
        fetch('/get-notification')
        .then(response => response.json())
        .then(data => {
            if (data.notifications) {
                const notificationList = document.getElementById('notification-list');
                notificationList.innerHTML = '';

                data.notifications.forEach(notification => {
                    const notificationItem = document.createElement('div');
                    notificationItem.classList.add('notification-item');

                    notificationItem.innerHTML = `
                        <h4>${notification.title}</h4>
                        <p>${notification.message}</p>
                        <small>Created at: ${notification.created_at}</small>
                    `;
                    notificationList.appendChild(notificationItem);
                });
            } else {
                // If no notifications are found
                notificationList.innerHTML = '<p>No notifications found.</p>';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}