# File generated from our OpenAPI spec by Stainless.

from typing import Dict, List, Union, Optional

from .._types import Timeout, NotGiven
from .._models import NoneModel, StringModel
from .._resource import SyncAPIResource, AsyncAPIResource
from ..pagination import SyncPage, AsyncPage
from ..types.card import *
from .._base_client import AsyncPaginator, make_request_options
from ..types.card_list_params import *
from ..types.card_embed_params import *
from ..types.card_create_params import *
from ..types.card_update_params import *
from ..types.card_reissue_params import *
from ..types.card_provision_params import *
from ..types.card_provision_response import *

__all__ = ["Cards", "AsyncCards"]


class Cards(SyncAPIResource):
    def create(
        self,
        body: CardCreateParams,
        *,
        headers: Union[Dict[str, str], NotGiven] = NotGiven(),
        max_retries: Union[int, NotGiven] = NotGiven(),
        timeout: Union[float, Timeout, None, NotGiven] = NotGiven(),
    ) -> Card:
        """Create a new virtual or physical card.

        Parameters `pin`, `shipping_address`, and `product_id` only apply to physical
        cards.
        """
        options = make_request_options(headers, max_retries, timeout)
        return self._post("/cards", model=Card, body=body, options=options)

    def retrieve(
        self,
        id: str,
        *,
        headers: Union[Dict[str, str], NotGiven] = NotGiven(),
        max_retries: Union[int, NotGiven] = NotGiven(),
        timeout: Union[float, Timeout, None, NotGiven] = NotGiven(),
    ) -> Card:
        """Get card configuration such as spend limit and state."""
        options = make_request_options(headers, max_retries, timeout)
        return self._get(f"/cards/{id}", model=Card, options=options)

    def update(
        self,
        id: str,
        body: CardUpdateParams,
        *,
        headers: Union[Dict[str, str], NotGiven] = NotGiven(),
        max_retries: Union[int, NotGiven] = NotGiven(),
        timeout: Union[float, Timeout, None, NotGiven] = NotGiven(),
    ) -> Card:
        """Update the specified properties of the card.

        Unsupplied properties will remain unchanged. `pin` parameter only applies to
        physical cards.

        _Note: setting a card to a `CLOSED` state is a final action that cannot be
        undone._
        """
        options = make_request_options(headers, max_retries, timeout)
        return self._patch(f"/cards/{id}", model=Card, body=body, options=options)

    def list(
        self,
        query: CardListParams = {},
        *,
        headers: Union[Dict[str, str], NotGiven] = NotGiven(),
        max_retries: Union[int, NotGiven] = NotGiven(),
        timeout: Union[float, Timeout, None, NotGiven] = NotGiven(),
    ) -> SyncPage[Card]:
        """List cards."""
        options = make_request_options(headers, max_retries, timeout)
        return self._get_api_list("/cards", model=Card, page=SyncPage[Card], query=query, options=options)

    def embed(
        self,
        query: CardEmbedParams = {},
        *,
        headers: Union[Dict[str, str], NotGiven] = NotGiven(),
        max_retries: Union[int, NotGiven] = NotGiven(),
        timeout: Union[float, Timeout, None, NotGiven] = NotGiven(),
    ) -> str:
        """
        Handling full card PANs and CVV codes requires that you comply with the Payment
        Card Industry Data Security Standards (PCI DSS). Some clients choose to reduce
        their compliance obligations by leveraging our embedded card UI solution
        documented below.

        In this setup, PANs and CVV codes are presented to the end-user via a card UI
        that we provide, optionally styled in the customer's branding using a specified
        css stylesheet. A user's browser makes the request directly to api.lithic.com,
        so card PANs and CVVs never touch the API customer's servers while full card
        data is displayed to their end-users. The response contains an HTML document.
        This means that the url for the request can be inserted straight into the `src`
        attribute of an iframe.

        ```html
        <iframe
          id="card-iframe"
          src="https://sandbox.lithic.com/v1/embed/card?embed_request=eyJjc3MiO...;hmac=r8tx1..."
          allow="clipboard-write"
          class="content"
        ></iframe>
        ```

        You should compute the request payload on the server side. You can render it (or
        the whole iframe) on the server or make an ajax call from your front end code,
        but **do not ever embed your API key into front end code, as doing so introduces
        a serious security vulnerability**.
        """
        headers = {"Accept": "text/html", **(headers or {})}
        options = make_request_options(headers, max_retries, timeout)
        result = self._get("/embed/card", model=StringModel, query=query, options=options)
        return result.content

    def provision(
        self,
        id: str,
        body: CardProvisionParams,
        *,
        headers: Union[Dict[str, str], NotGiven] = NotGiven(),
        max_retries: Union[int, NotGiven] = NotGiven(),
        timeout: Union[float, Timeout, None, NotGiven] = NotGiven(),
    ) -> CardProvisionResponse:
        """
        Allow your cardholders to directly add payment cards to the device's digital
        wallet (e.g. Apple Pay) with one touch from your app.

        This requires some additional setup and configuration. Reach out at
        [lithic.com/contact](https://lithic.com/contact) or your account rep for more
        information.
        """
        options = make_request_options(headers, max_retries, timeout)
        return self._post(f"/cards/{id}/provision", model=CardProvisionResponse, body=body, options=options)

    def reissue(
        self,
        id: str,
        body: CardReissueParams,
        *,
        headers: Union[Dict[str, str], NotGiven] = NotGiven(),
        max_retries: Union[int, NotGiven] = NotGiven(),
        timeout: Union[float, Timeout, None, NotGiven] = NotGiven(),
    ) -> Card:
        """Initiate print and shipment of a duplicate card.

        Only applies to cards of type `PHYSICAL` [beta].
        """
        options = make_request_options(headers, max_retries, timeout)
        return self._post(f"/cards/{id}/reissue", model=Card, body=body, options=options)


class AsyncCards(AsyncAPIResource):
    async def create(
        self,
        body: CardCreateParams,
        *,
        headers: Union[Dict[str, str], NotGiven] = NotGiven(),
        max_retries: Union[int, NotGiven] = NotGiven(),
        timeout: Union[float, Timeout, None, NotGiven] = NotGiven(),
    ) -> Card:
        """Create a new virtual or physical card.

        Parameters `pin`, `shipping_address`, and `product_id` only apply to physical
        cards.
        """
        options = make_request_options(headers, max_retries, timeout)
        return await self._post("/cards", model=Card, body=body, options=options)

    async def retrieve(
        self,
        id: str,
        *,
        headers: Union[Dict[str, str], NotGiven] = NotGiven(),
        max_retries: Union[int, NotGiven] = NotGiven(),
        timeout: Union[float, Timeout, None, NotGiven] = NotGiven(),
    ) -> Card:
        """Get card configuration such as spend limit and state."""
        options = make_request_options(headers, max_retries, timeout)
        return await self._get(f"/cards/{id}", model=Card, options=options)

    async def update(
        self,
        id: str,
        body: CardUpdateParams,
        *,
        headers: Union[Dict[str, str], NotGiven] = NotGiven(),
        max_retries: Union[int, NotGiven] = NotGiven(),
        timeout: Union[float, Timeout, None, NotGiven] = NotGiven(),
    ) -> Card:
        """Update the specified properties of the card.

        Unsupplied properties will remain unchanged. `pin` parameter only applies to
        physical cards.

        _Note: setting a card to a `CLOSED` state is a final action that cannot be
        undone._
        """
        options = make_request_options(headers, max_retries, timeout)
        return await self._patch(f"/cards/{id}", model=Card, body=body, options=options)

    def list(
        self,
        query: CardListParams = {},
        *,
        headers: Union[Dict[str, str], NotGiven] = NotGiven(),
        max_retries: Union[int, NotGiven] = NotGiven(),
        timeout: Union[float, Timeout, None, NotGiven] = NotGiven(),
    ) -> AsyncPaginator[Card, AsyncPage[Card]]:
        """List cards."""
        options = make_request_options(headers, max_retries, timeout)
        return self._get_api_list("/cards", model=Card, page=AsyncPage[Card], query=query, options=options)

    async def embed(
        self,
        query: CardEmbedParams = {},
        *,
        headers: Union[Dict[str, str], NotGiven] = NotGiven(),
        max_retries: Union[int, NotGiven] = NotGiven(),
        timeout: Union[float, Timeout, None, NotGiven] = NotGiven(),
    ) -> str:
        """
        Handling full card PANs and CVV codes requires that you comply with the Payment
        Card Industry Data Security Standards (PCI DSS). Some clients choose to reduce
        their compliance obligations by leveraging our embedded card UI solution
        documented below.

        In this setup, PANs and CVV codes are presented to the end-user via a card UI
        that we provide, optionally styled in the customer's branding using a specified
        css stylesheet. A user's browser makes the request directly to api.lithic.com,
        so card PANs and CVVs never touch the API customer's servers while full card
        data is displayed to their end-users. The response contains an HTML document.
        This means that the url for the request can be inserted straight into the `src`
        attribute of an iframe.

        ```html
        <iframe
          id="card-iframe"
          src="https://sandbox.lithic.com/v1/embed/card?embed_request=eyJjc3MiO...;hmac=r8tx1..."
          allow="clipboard-write"
          class="content"
        ></iframe>
        ```

        You should compute the request payload on the server side. You can render it (or
        the whole iframe) on the server or make an ajax call from your front end code,
        but **do not ever embed your API key into front end code, as doing so introduces
        a serious security vulnerability**.
        """
        headers = {"Accept": "text/html", **(headers or {})}
        options = make_request_options(headers, max_retries, timeout)
        result = await self._get("/embed/card", model=StringModel, query=query, options=options)
        return result.content

    async def provision(
        self,
        id: str,
        body: CardProvisionParams,
        *,
        headers: Union[Dict[str, str], NotGiven] = NotGiven(),
        max_retries: Union[int, NotGiven] = NotGiven(),
        timeout: Union[float, Timeout, None, NotGiven] = NotGiven(),
    ) -> CardProvisionResponse:
        """
        Allow your cardholders to directly add payment cards to the device's digital
        wallet (e.g. Apple Pay) with one touch from your app.

        This requires some additional setup and configuration. Reach out at
        [lithic.com/contact](https://lithic.com/contact) or your account rep for more
        information.
        """
        options = make_request_options(headers, max_retries, timeout)
        return await self._post(f"/cards/{id}/provision", model=CardProvisionResponse, body=body, options=options)

    async def reissue(
        self,
        id: str,
        body: CardReissueParams,
        *,
        headers: Union[Dict[str, str], NotGiven] = NotGiven(),
        max_retries: Union[int, NotGiven] = NotGiven(),
        timeout: Union[float, Timeout, None, NotGiven] = NotGiven(),
    ) -> Card:
        """Initiate print and shipment of a duplicate card.

        Only applies to cards of type `PHYSICAL` [beta].
        """
        options = make_request_options(headers, max_retries, timeout)
        return await self._post(f"/cards/{id}/reissue", model=Card, body=body, options=options)
