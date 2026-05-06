from django.db import models

class ActivityBlackListed(models.Model):
    """
    Originally sourced from Activity_BlackListed in /home/josh/PNDS_Interim_MIS-Data.accdb (13 records)
    """
    class Meta:
        db_table = "Activity_BlackListed"
    blacklistid = models.IntegerField(primary_key=True, db_column="BlacklistID")
    sectorid = models.IntegerField(null=True, blank=True, db_column="SectorID")
    # other fields...
