from objects.entities.opportunity.opportunity_address_request import OpportunityAddressRequest
from objects.entities.opportunity.opportunity_business_lines import OpportunityBusinessLines
from objects.entities.opportunity.opportunity_contact_request import OpportunityContactRequest
from objects.entities.opportunity.opportunity_document import OpportunityDocument
from tools.json_tools import extract


class QuoteRequest(OpportunityBusinessLines, OpportunityAddressRequest, OpportunityContactRequest, OpportunityDocument):
    def __init__(self, user):
        self._user = user
        self._code = 'O'
        self._id = None
        super().__init__(user, self._code)

    def post_new(self, legal_entity_id=None, payload=None):
        r = self.post_new_opportunity(legal_entity_id=legal_entity_id, body=payload)
        self._id = extract(body=r.json(), path="$..opportunityId")
        return r

    def get_quote_request_by_ids(self, opportunity=None, opportunity_id=None):
        if opportunity is None and opportunity_id is None:
            raise ValueError("Both opportunity or opportunity_id can't be None.")

        r = self.get_opportunity_by_id(opportunity=opportunity, opportunity_id=opportunity_id)
        return r

    def patch_request_address(self, opportunity=None, opportunity_id=None, payload=None):
        if opportunity is None and opportunity_id is None:
            raise ValueError("Both opportunity or opportunity_id can't be None.")
        r = self.patch_opportunity_address(opportunity=opportunity, opportunity_id=opportunity_id, payload=payload)
        return r

    def put_contact_request(self, opportunity=None, opportunity_id=None, payload=None):
        if opportunity is None and opportunity_id is None:
            raise ValueError("Both opportunity or opportunity_id can't be None.")
        r = self.put_opportunity_contact_request(opportunity=opportunity, opportunity_id=opportunity_id,
                                                 payload=payload)
        r = self.get_opportunity_by_id(opportunity=opportunity, opportunity_id=opportunity_id)
        return r

    def patch_project_document(self, opportunity=None, opportunity_id=None, file=None, test_data=None):
        if opportunity is None and opportunity_id is None:
            raise ValueError("Both opportunity or opportunity_id can't be None.")

        self.patch_opportunity_document(opportunity=opportunity,
                                        opportunity_id=opportunity_id,
                                        document_type="Project",
                                        file=file)

        r = self.patch_opportunity_document_dates_and_comment(opportunity=opportunity,
                                                              opportunity_id=opportunity_id,
                                                              test_data=test_data)
        r = self.get_opportunity_by_id(opportunity=opportunity, opportunity_id=opportunity_id)

        return r

    def patch_taxable_document(self, opportunity=None, opportunity_id=None, file=None):
        if opportunity is None and opportunity_id is None:
            raise ValueError("Both opportunity or opportunity_id can't be None.")

        self.patch_opportunity_document(opportunity=opportunity,
                                        opportunity_id=opportunity_id,
                                        document_type="Taxable",
                                        file=file)
        r = self.get_opportunity_by_id(opportunity=opportunity, opportunity_id=opportunity_id)

        return r
