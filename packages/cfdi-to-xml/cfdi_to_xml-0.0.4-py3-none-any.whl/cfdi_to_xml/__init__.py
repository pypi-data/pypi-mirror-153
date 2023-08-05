from multiprocessing.sharedctypes import Value
from typing import Union
from wsgiref.validate import validator

from xsdata.formats.dataclass.serializers.xml import XmlSerializer

from .cfdv40.comprobante import __NAMESPACE__
from .cfdv40.comprobante import Comprobante as ComprobanteXSD

NumberType = Union[float, int]


class Comprobante(ComprobanteXSD):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO why is it necessary to call post init?
        self.__post_init__()

    def __post_init__(self):
        # self._ensure_required_fields()
        self._compute_fields()

    def _ensure_required_fields(self) -> None:
        """Check all required fields are filled, otherwise raise a ValueError"""
        if not all(
            (
                self.fecha,
                self.moneda,
                self.lugar_expedicion,
                self.emisor,
                self.receptor,
                self.conceptos,
            )
        ):
            raise ValueError("Missing required fields")

    def _compute_fields(self):
        self.set_discount()
        self.set_amount_and_base_in_concepto()
        self.set_taxes_amount_in_concepto()
        self.set_taxes_amount_in_taxes()
        self.set_total_taxes_in_taxes()
        self.set_total_taxes()
        self.set_sub_total()
        self.set_total()

    def to_xml(self):
        """Renderizes XML file from class Comprobante, with "cfdi:" namespace"""
        serializer = XmlSerializer()
        xml_str = serializer.render(self, ns_map={"cfdi": __NAMESPACE__})
        # TODO improve prefixes mechanism
        xml_str = xml_str.replace("<Comprobante", "<cfdi:Comprobante")
        xml_str = xml_str.replace("</Comprobante", "</cfdi:Comprobante")
        xml_str = xml_str.replace("Concepto", "cfdi:Concepto")
        xml_str = xml_str.replace("cfdi:cfdi:Conceptos", "cfdi:Conceptos")
        xml_str = xml_str.replace("Traslados", "cfdi:Traslados")
        xml_str = xml_str.replace("Retenciones", "cfdi:Retenciones")
        return xml_str

    def compute_discount(self) -> NumberType:
        return (
            sum(concepto.descuento or 0 for concepto in self.conceptos.concepto)
            if self.conceptos
            else 0
        )

    def set_discount(self):
        """Sets the total amount of discount in Comprobante

        Raises:
            ValueError: If discount is negative, it raises an error
        """
        descuento = self.compute_discount()
        if descuento < 0:
            raise ValueError("Negative values in discounts are not admitted")
        self.descuento = round(descuento, 2)

    def set_amount_and_base_in_concepto(self):
        """Sets "Importe" for each Concepto and "Base" in Concepto taxes"""
        for concepto in self.conceptos.concepto:
            concepto.importe = compute_amount(  # TODO this will be better in the Concepto class
                qty=concepto.cantidad, unit_price=concepto.valor_unitario
            )
            # Set Base from Traslados in Concepto
            for traslado in concepto.impuestos.traslados.traslado:
                traslado.base = round(concepto.importe, 2)

    @staticmethod
    def compute_taxes_amount(*, base, tax_rate) -> NumberType:  # TODO analyze if really needed
        return base * tax_rate

    def set_taxes_amount_in_concepto(self):
        """Sets "Importe" for each Concepto taxes"""
        for concepto in self.conceptos.concepto:
            # ...from Traslados
            for traslado in concepto.impuestos.traslados.traslado:
                traslado.importe = (
                    self.compute_taxes_amount(  # TODO this will be better in the Traslado class
                        base=traslado.base, tax_rate=traslado.tasa_ocuota
                    )
                )
                traslado.importe = round(traslado.importe, 2)

    def compute_taxes_amount_in_16_taxes(self) -> NumberType:
        """Returns the total amount of all taxes with "0.16" as Tasa Ocuota"""
        return self._extracted_from_compute_taxes_amount_in_08_taxes_2(0.16)

    def compute_taxes_amount_in_08_taxes(self) -> NumberType:
        """Returns the total amount of all taxes with "0.08" as Tasa Ocuota"""
        return self._extracted_from_compute_taxes_amount_in_08_taxes_2(0.08)

    def _extracted_from_compute_taxes_amount_in_08_taxes_2(
        self, arg0
    ):  # TODO refactor, I think we can filter by tax CODE
        total = 0
        for concepto in self.conceptos.concepto:
            for traslado in concepto.impuestos.traslados.traslado:
                if traslado.tasa_ocuota == arg0:
                    total += traslado.base
        return total

    def set_taxes_amount_in_taxes(self):  # TODO this will be better in the Impuestos class
        """Sets "Importe" for each Tax in Taxes"""
        # ...from Traslados
        for traslado in self.impuestos.traslados.traslado:
            if traslado.tasa_ocuota == 0.16:
                traslado.base = round(self.compute_taxes_amount_in_16_taxes(), 2)
            elif traslado.tasa_ocuota == 0.08:
                traslado.base = round(self.compute_taxes_amount_in_08_taxes(), 2)
        return 0

    def set_total_taxes_in_taxes(self):
        """Sets the total amount for each tax in Taxes"""
        for traslado in self.impuestos.traslados.traslado:
            traslado.importe = (
                self.compute_taxes_amount(  # TODO this will be better in the Traslado class
                    base=traslado.base, tax_rate=traslado.tasa_ocuota
                )
            )
            traslado.importe = round(traslado.importe, 2)

    def compute_total_taxes(self) -> NumberType:
        total_taxes = 0.0
        if not self.conceptos:
            return 0
        for concepto in self.conceptos.concepto:
            # ...from Traslados
            if concepto.impuestos and concepto.impuestos.traslados:
                for traslado in concepto.impuestos.traslados.traslado:
                    total_taxes += traslado.importe or 0
        return total_taxes

    def set_total_taxes(self):
        """Sets the total amount of Trasladado taxes in Taxes"""
        self.impuestos.total_impuestos_trasladados = round(self.compute_total_taxes(), 2)

    def compute_sub_total(self) -> NumberType:
        return (
            sum(
                concepto.cantidad * concepto.valor_unitario
                if concepto.cantidad and concepto.valor_unitario
                else 0
                for concepto in self.conceptos.concepto
            )
            if self.conceptos
            else 0
        )

    def set_sub_total(self):
        self.sub_total = round(self.compute_sub_total(), 2)

    def compute_total(self) -> NumberType:
        total = (
            self.impuestos.total_impuestos_trasladados
            if self.impuestos and self.impuestos.total_impuestos_trasladados
            else 0
        ) + (self.sub_total or 0)
        total -= self.compute_discount()
        return total

    def set_total(self):
        self.total = round(self.compute_total(), 2)

    def sign(self, key, certificate, certificate_number):
        self.sello = key
        self.certificado = certificate
        self.no_certificado = certificate_number


def compute_amount(
    *, qty: NumberType, unit_price: NumberType
) -> NumberType:  # TODO analyze if really needed
    return qty * unit_price
