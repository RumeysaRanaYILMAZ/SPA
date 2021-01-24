from home.models import ServiceOffer, OfferSessions, Schedule
from serviceapp.Enums import Services, OfferStatus
from serviceapp.IDGenerator import IDGenerator as Generator
import datetime


class OfferController:
    serviceoffer = None

    def __init__(self, offid):
        try:
            self.serviceoffer = ServiceOffer.objects.filter(service_offer_id=offid).get()
        except Exception as e:
            print(e + "\nID ile obje bulunamadı.")

    @staticmethod
    def offer_add(cusid, advertid, customerconditions):
        guid = Generator.generate(Services.ServiceOffer)
        ServiceOffer(guid, cusid, advertid, customerconditions, OfferStatus.OFFERED).save()

    def offer_get(self):
        return self.serviceoffer

    def session_add(self, sessionid, customerid):
        availablesession = OfferSessions(self.serviceoffer.service_offer_id, sessionid)
        Schedule.objects.fiter(session_id=sessionid).customer_id = customerid
        availablesession.save()

    def providerscore_add(self, proscore):
        self.serviceoffer.provider_performance = proscore
        self.serviceoffer.save()

    def customerscore_add(self, custscore):
        self.serviceoffer.customer_performance = custscore
        self.serviceoffer.save()

    def offer_status_change(self, servstatus):
        self.serviceoffer.status = servstatus
        self.serviceoffer.save()

    @staticmethod
    def offer_get_by_stat(provid, status):
        ServiceOffer.objects.filter(adv_id__prov_id=provid, status=status)

    def date_passed(self):
        last_session = Schedule.objects.filter(expert_id=self.serviceoffer.adv_id__prov_id,
                                               customer_id=self.serviceoffer.purchaser).order_by('session_date',
                                                                                                 'hour').first()
        if last_session is not None and last_session.status == OfferStatus.ACCEPTED:
            if last_session.session_date > datetime.date.today() and last_session.hour < datetime.time.hour:
                self.offer_status_change(OfferStatus.DONE)
                return True
            else:
                return False
