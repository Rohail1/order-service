class OrderStatus:

    PENDING = 'Pending'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    COMPLETED = 'Completed'

    STATUSES = ['completed', 'accepted', 'pending', 'rejected']

    @classmethod
    def get_status(cls,  status):
        if status == 'completed':
            return cls.COMPLETED
        elif status == 'accepted':
            return cls.ACCEPTED
        elif status == 'rejected':
            return cls.REJECTED
        elif status == 'pending':
            return cls.PENDING
        else:
            return cls.PENDING
