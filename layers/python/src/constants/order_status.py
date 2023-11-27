class OrderStatus:

    PENDING = 'Pending'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    COMPLETED = 'Completed'

    STATUSES = ['completed', 'accepted', 'pending', 'rejected']

    def get_status(self,  status):
        if status == 'completed':
            return self.COMPLETED
        elif status == 'accepted':
            return self.ACCEPTED
        elif status == 'rejected':
            return self.REJECTED
        elif status == 'pending':
            return self.PENDING
        else:
            return self.PENDING
