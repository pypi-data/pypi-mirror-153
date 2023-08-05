from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional

from .c_exportacion import CExportacion
from .c_forma_pago import CFormaPago
from .c_impuesto import CImpuesto
from .c_meses import CMeses
from .c_metodo_pago import CMetodoPago
from .c_moneda import CMoneda
from .c_objeto_imp import CObjetoImp
from .c_pais import CPais
from .c_periodicidad import CPeriodicidad
from .c_regimen_fiscal import CRegimenFiscal
from .c_tipo_de_comprobante import CTipoDeComprobante
from .c_tipo_factor import CTipoFactor
from .c_tipo_relacion import CTipoRelacion
from .c_uso_cfdi import CUsoCfdi

__NAMESPACE__ = "http://www.sat.gob.mx/cfd/4"


@dataclass
class Comprobante:
    """
    Estándar de Comprobante Fiscal Digital por Internet.

    Attributes
        informacion_global: Nodo condicional para precisar la
            información relacionada con el comprobante global.
        cfdi_relacionados: Nodo opcional para precisar la información de
            los comprobantes relacionados.
        emisor: Nodo requerido para expresar la información del
            contribuyente emisor del comprobante.
        receptor: Nodo requerido para precisar la información del
            contribuyente receptor del comprobante.
        conceptos: Nodo requerido para listar los conceptos cubiertos
            por el comprobante.
        impuestos: Nodo condicional para expresar el resumen de los
            impuestos aplicables.
        complemento: Nodo opcional donde se incluye el complemento
            Timbre Fiscal Digital de manera obligatoria y los nodos
            complementarios determinados por el SAT, de acuerdo con las
            disposiciones particulares para un sector o actividad
            específica.
        addenda: Nodo opcional para recibir las extensiones al presente
            formato que sean de utilidad al contribuyente. Para las
            reglas de uso del mismo, referirse al formato origen.
        version: Atributo requerido con valor prefijado a 4.0 que indica
            la versión del estándar bajo el que se encuentra expresado
            el comprobante.
        serie: Atributo opcional para precisar la serie para control
            interno del contribuyente. Este atributo acepta una cadena
            de caracteres.
        folio: Atributo opcional para control interno del contribuyente
            que expresa el folio del comprobante, acepta una cadena de
            caracteres.
        fecha: Atributo requerido para la expresión de la fecha y hora
            de expedición del Comprobante Fiscal Digital por Internet.
            Se expresa en la forma AAAA-MM-DDThh:mm:ss y debe
            corresponder con la hora local donde se expide el
            comprobante.
        sello: Atributo requerido para contener el sello digital del
            comprobante fiscal, al que hacen referencia las reglas de
            resolución miscelánea vigente. El sello debe ser expresado
            como una cadena de texto en formato Base 64.
        forma_pago: Atributo condicional para expresar la clave de la
            forma de pago de los bienes o servicios amparados por el
            comprobante.
        no_certificado: Atributo requerido para expresar el número de
            serie del certificado de sello digital que ampara al
            comprobante, de acuerdo con el acuse correspondiente a 20
            posiciones otorgado por el sistema del SAT.
        certificado: Atributo requerido que sirve para incorporar el
            certificado de sello digital que ampara al comprobante, como
            texto en formato base 64.
        condiciones_de_pago: Atributo condicional para expresar las
            condiciones comerciales aplicables para el pago del
            comprobante fiscal digital por Internet. Este atributo puede
            ser condicionado mediante atributos o complementos.
        sub_total: Atributo requerido para representar la suma de los
            importes de los conceptos antes de descuentos e impuesto. No
            se permiten valores negativos.
        descuento: Atributo condicional para representar el importe
            total de los descuentos aplicables antes de impuestos. No se
            permiten valores negativos. Se debe registrar cuando existan
            conceptos con descuento.
        moneda: Atributo requerido para identificar la clave de la
            moneda utilizada para expresar los montos, cuando se usa
            moneda nacional se registra MXN. Conforme con la
            especificación ISO 4217.
        tipo_cambio: Atributo condicional para representar el tipo de
            cambio FIX conforme con la moneda usada. Es requerido cuando
            la clave de moneda es distinta de MXN y de XXX. El valor
            debe reflejar el número de pesos mexicanos que equivalen a
            una unidad de la divisa señalada en el atributo moneda. Si
            el valor está fuera del porcentaje aplicable a la moneda
            tomado del catálogo c_Moneda, el emisor debe obtener del PAC
            que vaya a timbrar el CFDI, de manera no automática, una
            clave de confirmación para ratificar que el valor es
            correcto e integrar dicha clave en el atributo Confirmacion.
        total: Atributo requerido para representar la suma del subtotal,
            menos los descuentos aplicables, más las contribuciones
            recibidas (impuestos trasladados - federales y/o locales,
            derechos, productos, aprovechamientos, aportaciones de
            seguridad social, contribuciones de mejoras) menos los
            impuestos retenidos federales y/o locales. Si el valor es
            superior al límite que establezca el SAT en la Resolución
            Miscelánea Fiscal vigente, el emisor debe obtener del PAC
            que vaya a timbrar el CFDI, de manera no automática, una
            clave de confirmación para ratificar que el valor es
            correcto e integrar dicha clave en el atributo Confirmacion.
            No se permiten valores negativos.
        tipo_de_comprobante: Atributo requerido para expresar la clave
            del efecto del comprobante fiscal para el contribuyente
            emisor.
        exportacion: Atributo requerido para expresar si el comprobante
            ampara una operación de exportación.
        metodo_pago: Atributo condicional para precisar la clave del
            método de pago que aplica para este comprobante fiscal
            digital por Internet, conforme al Artículo 29-A fracción VII
            incisos a y b del CFF.
        lugar_expedicion: Atributo requerido para incorporar el código
            postal del lugar de expedición del comprobante (domicilio de
            la matriz o de la sucursal).
        confirmacion: Atributo condicional para registrar la clave de
            confirmación que entregue el PAC para expedir el comprobante
            con importes grandes, con un tipo de cambio fuera del rango
            establecido o con ambos casos. Es requerido cuando se
            registra un tipo de cambio o un total fuera del rango
            establecido.
    """

    class Meta:
        namespace = "http://www.sat.gob.mx/cfd/4"

    informacion_global: Optional["Comprobante.InformacionGlobal"] = field(
        default=None,
        metadata={
            "name": "InformacionGlobal",
            "type": "Element",
        },
    )
    cfdi_relacionados: List["Comprobante.CfdiRelacionados"] = field(
        default_factory=list,
        metadata={
            "name": "CfdiRelacionados",
            "type": "Element",
        },
    )
    emisor: Optional["Comprobante.Emisor"] = field(
        default=None,
        metadata={
            "name": "Emisor",
            "type": "Element",
            "required": True,
        },
    )
    receptor: Optional["Comprobante.Receptor"] = field(
        default=None,
        metadata={
            "name": "Receptor",
            "type": "Element",
            "required": True,
        },
    )
    conceptos: Optional["Comprobante.Conceptos"] = field(
        default=None,
        metadata={
            "name": "Conceptos",
            "type": "Element",
            "required": True,
        },
    )
    impuestos: Optional["Comprobante.Impuestos"] = field(
        default=None,
        metadata={
            "name": "Impuestos",
            "type": "Element",
        },
    )
    complemento: Optional["Comprobante.Complemento"] = field(
        default=None,
        metadata={
            "name": "Complemento",
            "type": "Element",
        },
    )
    addenda: Optional["Comprobante.Addenda"] = field(
        default=None,
        metadata={
            "name": "Addenda",
            "type": "Element",
        },
    )
    version: str = field(
        init=False,
        default="4.0",
        metadata={
            "name": "Version",
            "type": "Attribute",
            "required": True,
            "white_space": "collapse",
        },
    )
    serie: Optional[str] = field(
        default=None,
        metadata={
            "name": "Serie",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 25,
            "white_space": "collapse",
            "pattern": r"[^|]{1,25}",
        },
    )
    folio: Optional[str] = field(
        default=None,
        metadata={
            "name": "Folio",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 40,
            "white_space": "collapse",
            "pattern": r"[^|]{1,40}",
        },
    )
    fecha: Optional[str] = field(
        default=None,
        metadata={
            "name": "Fecha",
            "type": "Attribute",
            "required": True,
            "white_space": "collapse",
            "pattern": r"(20[1-9][0-9])-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T(([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9])",
        },
    )
    sello: Optional[str] = field(
        default=None,
        metadata={
            "name": "Sello",
            "type": "Attribute",
            "required": True,
            "white_space": "collapse",
        },
    )
    forma_pago: Optional[CFormaPago] = field(
        default=None,
        metadata={
            "name": "FormaPago",
            "type": "Attribute",
        },
    )
    no_certificado: Optional[str] = field(
        default=None,
        metadata={
            "name": "NoCertificado",
            "type": "Attribute",
            "required": True,
            "length": 20,
            "white_space": "collapse",
            "pattern": r"[0-9]{20}",
        },
    )
    certificado: Optional[str] = field(
        default=None,
        metadata={
            "name": "Certificado",
            "type": "Attribute",
            "required": True,
            "white_space": "collapse",
        },
    )
    condiciones_de_pago: Optional[str] = field(
        default=None,
        metadata={
            "name": "CondicionesDePago",
            "type": "Attribute",
            "min_length": 1,
            "max_length": 1000,
            "white_space": "collapse",
            "pattern": r"[^|]{1,1000}",
        },
    )
    sub_total: Optional[float] = field(
        default=None,
        metadata={
            "name": "SubTotal",
            "type": "Attribute",
            "required": True,
            "min_inclusive": "0.000000",
            "fraction_digits": 6,
            "white_space": "collapse",
            "pattern": r"[0-9]{1,18}(.[0-9]{1,6})?",
        },
    )
    descuento: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descuento",
            "type": "Attribute",
            "min_inclusive": "0.000000",
            "fraction_digits": 6,
            "white_space": "collapse",
            "pattern": r"[0-9]{1,18}(.[0-9]{1,6})?",
        },
    )
    moneda: Optional[CMoneda] = field(
        default=None,
        metadata={
            "name": "Moneda",
            "type": "Attribute",
            "required": True,
        },
    )
    tipo_cambio: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "TipoCambio",
            "type": "Attribute",
            "min_inclusive": Decimal("0.000001"),
            "fraction_digits": 6,
            "white_space": "collapse",
        },
    )
    total: Optional[str] = field(
        default=None,
        metadata={
            "name": "Total",
            "type": "Attribute",
            "required": True,
            "min_inclusive": "0.000000",
            "fraction_digits": 6,
            "white_space": "collapse",
            "pattern": r"[0-9]{1,18}(.[0-9]{1,6})?",
        },
    )
    tipo_de_comprobante: Optional[CTipoDeComprobante] = field(
        default=None,
        metadata={
            "name": "TipoDeComprobante",
            "type": "Attribute",
            "required": True,
        },
    )
    exportacion: Optional[CExportacion] = field(
        default=None,
        metadata={
            "name": "Exportacion",
            "type": "Attribute",
            "required": True,
        },
    )
    metodo_pago: Optional[CMetodoPago] = field(
        default=None,
        metadata={
            "name": "MetodoPago",
            "type": "Attribute",
        },
    )
    lugar_expedicion: Optional[str] = field(
        default=None,
        metadata={
            "name": "LugarExpedicion",
            "type": "Attribute",
            "required": True,
        },
    )
    confirmacion: Optional[str] = field(
        default=None,
        metadata={
            "name": "Confirmacion",
            "type": "Attribute",
            "length": 5,
            "white_space": "collapse",
            "pattern": r"[0-9a-zA-Z]{5}",
        },
    )

    @dataclass
    class InformacionGlobal:
        """
        Attributes
            periodicidad: Atributo requerido para expresar el período al
                que corresponde la información del comprobante global.
            meses: Atributo requerido para expresar el mes o los meses
                al que corresponde la información del comprobante
                global.
            a_o: Atributo requerido para expresar el año al que
                corresponde la información del comprobante global.
        """

        periodicidad: Optional[CPeriodicidad] = field(
            default=None,
            metadata={
                "name": "Periodicidad",
                "type": "Attribute",
                "required": True,
            },
        )
        meses: Optional[CMeses] = field(
            default=None,
            metadata={
                "name": "Meses",
                "type": "Attribute",
                "required": True,
            },
        )
        a_o: Optional[int] = field(
            default=None,
            metadata={
                "name": "Año",
                "type": "Attribute",
                "required": True,
                "min_inclusive": 2021,
                "white_space": "collapse",
            },
        )

    @dataclass
    class CfdiRelacionados:
        """
        Attributes
            cfdi_relacionado: Nodo requerido para precisar la
                información de los comprobantes relacionados.
            tipo_relacion: Atributo requerido para indicar la clave de
                la relación que existe entre éste que se está generando
                y el o los CFDI previos.
        """

        cfdi_relacionado: List["Comprobante.CfdiRelacionados.CfdiRelacionado"] = field(
            default_factory=list,
            metadata={
                "name": "CfdiRelacionado",
                "type": "Element",
                "min_occurs": 1,
            },
        )
        tipo_relacion: Optional[CTipoRelacion] = field(
            default=None,
            metadata={
                "name": "TipoRelacion",
                "type": "Attribute",
                "required": True,
            },
        )

        @dataclass
        class CfdiRelacionado:
            """
            Attributes
                uuid: Atributo requerido para registrar el folio fiscal
                    (UUID) de un CFDI relacionado con el presente
                    comprobante, por ejemplo: Si el CFDI relacionado es
                    un comprobante de traslado que sirve para registrar
                    el movimiento de la mercancía. Si este comprobante
                    se usa como nota de crédito o nota de débito del
                    comprobante relacionado. Si este comprobante es una
                    devolución sobre el comprobante relacionado. Si éste
                    sustituye a una factura cancelada.
            """

            uuid: Optional[str] = field(
                default=None,
                metadata={
                    "name": "UUID",
                    "type": "Attribute",
                    "required": True,
                    "length": 36,
                    "white_space": "collapse",
                    "pattern": r"[a-f0-9A-F]{8}-[a-f0-9A-F]{4}-[a-f0-9A-F]{4}-[a-f0-9A-F]{4}-[a-f0-9A-F]{12}",
                },
            )

    @dataclass
    class Emisor:
        """
        Attributes
            rfc: Atributo requerido para registrar la Clave del Registro
                Federal de Contribuyentes correspondiente al
                contribuyente emisor del comprobante.
            nombre: Atributo requerido para registrar el nombre,
                denominación o razón social del contribuyente inscrito
                en el RFC, del emisor del comprobante.
            regimen_fiscal: Atributo requerido para incorporar la clave
                del régimen del contribuyente emisor al que aplicará el
                efecto fiscal de este comprobante.
            fac_atr_adquirente: Atributo condicional para expresar el
                número de operación proporcionado por el SAT cuando se
                trate de un comprobante a través de un PCECFDI o un
                PCGCFDISP.
        """

        rfc: Optional[str] = field(
            default=None,
            metadata={
                "name": "Rfc",
                "type": "Attribute",
                "required": True,
                "min_length": 12,
                "max_length": 13,
                "white_space": "collapse",
                "pattern": r"[A-Z&Ñ]{3,4}[0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])[A-Z0-9]{2}[0-9A]",
            },
        )
        nombre: Optional[str] = field(
            default=None,
            metadata={
                "name": "Nombre",
                "type": "Attribute",
                "required": True,
                "min_length": 1,
                "max_length": 300,
                "white_space": "collapse",
                "pattern": r"[^|]{1,300}",
            },
        )
        regimen_fiscal: Optional[CRegimenFiscal] = field(
            default=None,
            metadata={
                "name": "RegimenFiscal",
                "type": "Attribute",
                "required": True,
            },
        )
        fac_atr_adquirente: Optional[str] = field(
            default=None,
            metadata={
                "name": "FacAtrAdquirente",
                "type": "Attribute",
                "length": 10,
                "white_space": "collapse",
                "pattern": r"[0-9]{10}",
            },
        )

    @dataclass
    class Receptor:
        """
        Attributes
            rfc: Atributo requerido para registrar la Clave del Registro
                Federal de Contribuyentes correspondiente al
                contribuyente receptor del comprobante.
            nombre: Atributo requerido para registrar el nombre(s),
                primer apellido, segundo apellido, según corresponda,
                denominación o razón social del contribuyente, inscrito
                en el RFC, del receptor del comprobante.
            domicilio_fiscal_receptor: Atributo requerido para registrar
                el código postal del domicilio fiscal del receptor del
                comprobante.
            residencia_fiscal: Atributo condicional para registrar la
                clave del país de residencia para efectos fiscales del
                receptor del comprobante, cuando se trate de un
                extranjero, y que es conforme con la especificación ISO
                3166-1 alpha-3. Es requerido cuando se incluya el
                complemento de comercio exterior o se registre el
                atributo NumRegIdTrib.
            num_reg_id_trib: Atributo condicional para expresar el
                número de registro de identidad fiscal del receptor
                cuando sea residente en el extranjero. Es requerido
                cuando se incluya el complemento de comercio exterior.
            regimen_fiscal_receptor: Atributo requerido para incorporar
                la clave del régimen fiscal del contribuyente receptor
                al que aplicará el efecto fiscal de este comprobante.
            uso_cfdi: Atributo requerido para expresar la clave del uso
                que dará a esta factura el receptor del CFDI.
        """

        rfc: Optional[str] = field(
            default=None,
            metadata={
                "name": "Rfc",
                "type": "Attribute",
                "required": True,
                "min_length": 12,
                "max_length": 13,
                "white_space": "collapse",
                "pattern": r"[A-Z&Ñ]{3,4}[0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])[A-Z0-9]{2}[0-9A]",
            },
        )
        nombre: Optional[str] = field(
            default=None,
            metadata={
                "name": "Nombre",
                "type": "Attribute",
                "required": True,
                "min_length": 1,
                "max_length": 300,
                "white_space": "collapse",
                "pattern": r"[^|]{1,300}",
            },
        )
        domicilio_fiscal_receptor: Optional[str] = field(
            default=None,
            metadata={
                "name": "DomicilioFiscalReceptor",
                "type": "Attribute",
                "required": True,
                "length": 5,
                "white_space": "collapse",
                "pattern": r"[0-9]{5}",
            },
        )
        residencia_fiscal: Optional[CPais] = field(
            default=None,
            metadata={
                "name": "ResidenciaFiscal",
                "type": "Attribute",
            },
        )
        num_reg_id_trib: Optional[str] = field(
            default=None,
            metadata={
                "name": "NumRegIdTrib",
                "type": "Attribute",
                "min_length": 1,
                "max_length": 40,
                "white_space": "collapse",
            },
        )
        regimen_fiscal_receptor: Optional[CRegimenFiscal] = field(
            default=None,
            metadata={
                "name": "RegimenFiscalReceptor",
                "type": "Attribute",
                "required": True,
            },
        )
        uso_cfdi: Optional[CUsoCfdi] = field(
            default=None,
            metadata={
                "name": "UsoCFDI",
                "type": "Attribute",
                "required": True,
            },
        )

    @dataclass
    class Conceptos:
        """
        Attributes
            concepto: Nodo requerido para registrar la información
                detallada de un bien o servicio amparado en el
                comprobante.
        """

        concepto: List["Comprobante.Conceptos.Concepto"] = field(
            default_factory=list,
            metadata={
                "name": "Concepto",
                "type": "Element",
                "min_occurs": 1,
            },
        )

        @dataclass
        class Concepto:
            """
            Attributes
                impuestos: Nodo condicional para capturar los impuestos
                    aplicables al presente concepto.
                acuenta_terceros: Nodo opcional para registrar
                    información del contribuyente Tercero, a cuenta del
                    que se realiza la operación.
                informacion_aduanera: Nodo opcional para introducir la
                    información aduanera aplicable cuando se trate de
                    ventas de primera mano de mercancías importadas o se
                    trate de operaciones de comercio exterior con bienes
                    o servicios.
                cuenta_predial: Nodo opcional para asentar el número de
                    cuenta predial con el que fue registrado el
                    inmueble, en el sistema catastral de la entidad
                    federativa de que trate, o bien para incorporar los
                    datos de identificación del certificado de
                    participación inmobiliaria no amortizable.
                complemento_concepto: Nodo opcional donde se incluyen
                    los nodos complementarios de extensión al concepto
                    definidos por el SAT, de acuerdo con las
                    disposiciones particulares para un sector o
                    actividad específica.
                parte: Nodo opcional para expresar las partes o
                    componentes que integran la totalidad del concepto
                    expresado en el comprobante fiscal digital por
                    Internet.
                clave_prod_serv: Atributo requerido para expresar la
                    clave del producto o del servicio amparado por el
                    presente concepto. Es requerido y deben utilizar las
                    claves del catálogo de productos y servicios, cuando
                    los conceptos que registren por sus actividades
                    correspondan con dichos conceptos.
                no_identificacion: Atributo opcional para expresar el
                    número de parte, identificador del producto o del
                    servicio, la clave de producto o servicio, SKU o
                    equivalente, propia de la operación del emisor,
                    amparado por el presente concepto. Opcionalmente se
                    puede utilizar claves del estándar GTIN.
                cantidad: Atributo requerido para precisar la cantidad
                    de bienes o servicios del tipo particular definido
                    por el presente concepto.
                clave_unidad: Atributo requerido para precisar la clave
                    de unidad de medida estandarizada aplicable para la
                    cantidad expresada en el concepto. La unidad debe
                    corresponder con la descripción del concepto.
                unidad: Atributo opcional para precisar la unidad de
                    medida propia de la operación del emisor, aplicable
                    para la cantidad expresada en el concepto. La unidad
                    debe corresponder con la descripción del concepto.
                descripcion: Atributo requerido para precisar la
                    descripción del bien o servicio cubierto por el
                    presente concepto.
                valor_unitario: Atributo requerido para precisar el
                    valor o precio unitario del bien o servicio cubierto
                    por el presente concepto.
                importe: Atributo requerido para precisar el importe
                    total de los bienes o servicios del presente
                    concepto. Debe ser equivalente al resultado de
                    multiplicar la cantidad por el valor unitario
                    expresado en el concepto. No se permiten valores
                    negativos.
                descuento: Atributo opcional para representar el importe
                    de los descuentos aplicables al concepto. No se
                    permiten valores negativos.
                objeto_imp: Atributo requerido para expresar si la
                    operación comercial es objeto o no de impuesto.
            """

            impuestos: Optional["Comprobante.Conceptos.Concepto.Impuestos"] = field(
                default=None,
                metadata={
                    "name": "Impuestos",
                    "type": "Element",
                },
            )
            acuenta_terceros: Optional["Comprobante.Conceptos.Concepto.AcuentaTerceros"] = field(
                default=None,
                metadata={
                    "name": "ACuentaTerceros",
                    "type": "Element",
                },
            )
            informacion_aduanera: List[
                "Comprobante.Conceptos.Concepto.InformacionAduanera"
            ] = field(
                default_factory=list,
                metadata={
                    "name": "InformacionAduanera",
                    "type": "Element",
                },
            )
            cuenta_predial: List["Comprobante.Conceptos.Concepto.CuentaPredial"] = field(
                default_factory=list,
                metadata={
                    "name": "CuentaPredial",
                    "type": "Element",
                },
            )
            complemento_concepto: Optional[
                "Comprobante.Conceptos.Concepto.ComplementoConcepto"
            ] = field(
                default=None,
                metadata={
                    "name": "ComplementoConcepto",
                    "type": "Element",
                },
            )
            parte: List["Comprobante.Conceptos.Concepto.Parte"] = field(
                default_factory=list,
                metadata={
                    "name": "Parte",
                    "type": "Element",
                },
            )
            clave_prod_serv: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ClaveProdServ",
                    "type": "Attribute",
                    "required": True,
                },
            )
            no_identificacion: Optional[str] = field(
                default=None,
                metadata={
                    "name": "NoIdentificacion",
                    "type": "Attribute",
                    "min_length": 1,
                    "max_length": 100,
                    "white_space": "collapse",
                    "pattern": r"[^|]{1,100}",
                },
            )
            cantidad: Optional[float] = field(
                default=None,
                metadata={
                    "name": "Cantidad",
                    "type": "Attribute",
                    "required": True,
                    "min_inclusive": Decimal("0.000001"),
                    "fraction_digits": 6,
                    "white_space": "collapse",
                },
            )
            clave_unidad: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ClaveUnidad",
                    "type": "Attribute",
                    "required": True,
                },
            )
            unidad: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Unidad",
                    "type": "Attribute",
                    "min_length": 1,
                    "max_length": 20,
                    "white_space": "collapse",
                    "pattern": r"[^|]{1,20}",
                },
            )
            descripcion: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Descripcion",
                    "type": "Attribute",
                    "required": True,
                    "min_length": 1,
                    "max_length": 1000,
                    "white_space": "collapse",
                    "pattern": r"[^|]{1,1000}",
                },
            )
            valor_unitario: Optional[float] = field(
                default=None,
                metadata={
                    "name": "ValorUnitario",
                    "type": "Attribute",
                    "required": True,
                    "min_inclusive": "0.000000",
                    "fraction_digits": 6,
                    "white_space": "collapse",
                    "pattern": r"[0-9]{1,18}(.[0-9]{1,6})?",
                },
            )
            importe: Optional[float] = field(
                default=None,
                metadata={
                    "name": "Importe",
                    "type": "Attribute",
                    "required": True,
                    "min_inclusive": "0.000000",
                    "fraction_digits": 6,
                    "white_space": "collapse",
                    "pattern": r"[0-9]{1,18}(.[0-9]{1,6})?",
                },
            )
            descuento: Optional[float] = field(
                default=None,
                metadata={
                    "name": "Descuento",
                    "type": "Attribute",
                    "min_inclusive": "0.000000",
                    "fraction_digits": 6,
                    "white_space": "collapse",
                    "pattern": r"[0-9]{1,18}(.[0-9]{1,6})?",
                },
            )
            objeto_imp: Optional[CObjetoImp] = field(
                default=None,
                metadata={
                    "name": "ObjetoImp",
                    "type": "Attribute",
                    "required": True,
                },
            )

            @dataclass
            class Impuestos:
                """
                Attributes
                    traslados: Nodo opcional para asentar los impuestos
                        trasladados aplicables al presente concepto.
                    retenciones: Nodo opcional para asentar los
                        impuestos retenidos aplicables al presente
                        concepto.
                """

                traslados: Optional["Comprobante.Conceptos.Concepto.Impuestos.Traslados"] = field(
                    default=None,
                    metadata={
                        "name": "Traslados",
                        "type": "Element",
                    },
                )
                retenciones: Optional[
                    "Comprobante.Conceptos.Concepto.Impuestos.Retenciones"
                ] = field(
                    default=None,
                    metadata={
                        "name": "Retenciones",
                        "type": "Element",
                    },
                )

                @dataclass
                class Traslados:
                    """
                    Attributes
                        traslado: Nodo requerido para asentar la
                            información detallada de un traslado de
                            impuestos aplicable al presente concepto.
                    """

                    traslado: List[
                        "Comprobante.Conceptos.Concepto.Impuestos.Traslados.Traslado"
                    ] = field(
                        default_factory=list,
                        metadata={
                            "name": "Traslado",
                            "type": "Element",
                            "min_occurs": 1,
                        },
                    )

                    @dataclass
                    class Traslado:
                        """
                        Attributes
                            base: Atributo requerido para señalar la
                                base para el cálculo del impuesto, la
                                determinación de la base se realiza de
                                acuerdo con las disposiciones fiscales
                                vigentes. No se permiten valores
                                negativos.
                            impuesto: Atributo requerido para señalar la
                                clave del tipo de impuesto trasladado
                                aplicable al concepto.
                            tipo_factor: Atributo requerido para señalar
                                la clave del tipo de factor que se
                                aplica a la base del impuesto.
                            tasa_ocuota: Atributo condicional para
                                señalar el valor de la tasa o cuota del
                                impuesto que se traslada para el
                                presente concepto. Es requerido cuando
                                el atributo TipoFactor tenga una clave
                                que corresponda a Tasa o Cuota.
                            importe: Atributo condicional para señalar
                                el importe del impuesto trasladado que
                                aplica al concepto. No se permiten
                                valores negativos. Es requerido cuando
                                TipoFactor sea Tasa o Cuota.
                        """

                        base: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "Base",
                                "type": "Attribute",
                                "required": True,
                                "min_inclusive": Decimal("0.000001"),
                                "fraction_digits": 6,
                                "white_space": "collapse",
                            },
                        )
                        impuesto: Optional[CImpuesto] = field(
                            default=None,
                            metadata={
                                "name": "Impuesto",
                                "type": "Attribute",
                                "required": True,
                            },
                        )
                        tipo_factor: Optional[CTipoFactor] = field(
                            default=None,
                            metadata={
                                "name": "TipoFactor",
                                "type": "Attribute",
                                "required": True,
                            },
                        )
                        tasa_ocuota: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "TasaOCuota",
                                "type": "Attribute",
                                "min_inclusive": Decimal("0.000000"),
                                "fraction_digits": 6,
                                "white_space": "collapse",
                            },
                        )
                        importe: Optional[float] = field(
                            default=None,
                            metadata={
                                "name": "Importe",
                                "type": "Attribute",
                                "min_inclusive": "0.000000",
                                "fraction_digits": 6,
                                "white_space": "collapse",
                                "pattern": r"[0-9]{1,18}(.[0-9]{1,6})?",
                            },
                        )

                @dataclass
                class Retenciones:
                    """
                    Attributes
                        retencion: Nodo requerido para asentar la
                            información detallada de una retención de
                            impuestos aplicable al presente concepto.
                    """

                    retencion: List[
                        "Comprobante.Conceptos.Concepto.Impuestos.Retenciones.Retencion"
                    ] = field(
                        default_factory=list,
                        metadata={
                            "name": "Retencion",
                            "type": "Element",
                            "min_occurs": 1,
                        },
                    )

                    @dataclass
                    class Retencion:
                        """
                        Attributes
                            base: Atributo requerido para señalar la
                                base para el cálculo de la retención, la
                                determinación de la base se realiza de
                                acuerdo con las disposiciones fiscales
                                vigentes. No se permiten valores
                                negativos.
                            impuesto: Atributo requerido para señalar la
                                clave del tipo de impuesto retenido
                                aplicable al concepto.
                            tipo_factor: Atributo requerido para señalar
                                la clave del tipo de factor que se
                                aplica a la base del impuesto.
                            tasa_ocuota: Atributo requerido para señalar
                                la tasa o cuota del impuesto que se
                                retiene para el presente concepto.
                            importe: Atributo requerido para señalar el
                                importe del impuesto retenido que aplica
                                al concepto. No se permiten valores
                                negativos.
                        """

                        base: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "Base",
                                "type": "Attribute",
                                "required": True,
                                "min_inclusive": Decimal("0.000001"),
                                "fraction_digits": 6,
                                "white_space": "collapse",
                            },
                        )
                        impuesto: Optional[CImpuesto] = field(
                            default=None,
                            metadata={
                                "name": "Impuesto",
                                "type": "Attribute",
                                "required": True,
                            },
                        )
                        tipo_factor: Optional[CTipoFactor] = field(
                            default=None,
                            metadata={
                                "name": "TipoFactor",
                                "type": "Attribute",
                                "required": True,
                            },
                        )
                        tasa_ocuota: Optional[Decimal] = field(
                            default=None,
                            metadata={
                                "name": "TasaOCuota",
                                "type": "Attribute",
                                "required": True,
                                "min_inclusive": Decimal("0.000000"),
                                "fraction_digits": 6,
                                "white_space": "collapse",
                            },
                        )
                        importe: Optional[str] = field(
                            default=None,
                            metadata={
                                "name": "Importe",
                                "type": "Attribute",
                                "required": True,
                                "min_inclusive": "0.000000",
                                "fraction_digits": 6,
                                "white_space": "collapse",
                                "pattern": r"[0-9]{1,18}(.[0-9]{1,6})?",
                            },
                        )

            @dataclass
            class AcuentaTerceros:
                """
                Attributes
                    rfc_acuenta_terceros: Atributo requerido para
                        registrar la Clave del Registro Federal de
                        Contribuyentes del contribuyente Tercero, a
                        cuenta del que se realiza la operación.
                    nombre_acuenta_terceros: Atributo requerido para
                        registrar el nombre, denominación o razón social
                        del contribuyente Tercero correspondiente con el
                        Rfc, a cuenta del que se realiza la operación.
                    regimen_fiscal_acuenta_terceros: Atributo requerido
                        para incorporar la clave del régimen del
                        contribuyente Tercero, a cuenta del que se
                        realiza la operación.
                    domicilio_fiscal_acuenta_terceros: Atributo
                        requerido para incorporar el código postal del
                        domicilio fiscal del Tercero, a cuenta del que
                        se realiza la operación.
                """

                rfc_acuenta_terceros: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "RfcACuentaTerceros",
                        "type": "Attribute",
                        "required": True,
                        "min_length": 12,
                        "max_length": 13,
                        "white_space": "collapse",
                        "pattern": r"[A-Z&Ñ]{3,4}[0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])[A-Z0-9]{2}[0-9A]",
                    },
                )
                nombre_acuenta_terceros: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "NombreACuentaTerceros",
                        "type": "Attribute",
                        "required": True,
                        "min_length": 1,
                        "max_length": 300,
                        "white_space": "collapse",
                        "pattern": r"[^|]{1,300}",
                    },
                )
                regimen_fiscal_acuenta_terceros: Optional[CRegimenFiscal] = field(
                    default=None,
                    metadata={
                        "name": "RegimenFiscalACuentaTerceros",
                        "type": "Attribute",
                        "required": True,
                    },
                )
                domicilio_fiscal_acuenta_terceros: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "DomicilioFiscalACuentaTerceros",
                        "type": "Attribute",
                        "required": True,
                        "length": 5,
                        "white_space": "collapse",
                        "pattern": r"[0-9]{5}",
                    },
                )

            @dataclass
            class InformacionAduanera:
                """
                Attributes
                    numero_pedimento: Atributo requerido para expresar
                        el número del pedimento que ampara la
                        importación del bien que se expresa en el
                        siguiente formato: últimos 2 dígitos del año de
                        validación seguidos por dos espacios, 2 dígitos
                        de la aduana de despacho seguidos por dos
                        espacios, 4 dígitos del número de la patente
                        seguidos por dos espacios, 1 dígito que
                        corresponde al último dígito del año en curso,
                        salvo que se trate de un pedimento consolidado
                        iniciado en el año inmediato anterior o del
                        pedimento original de una rectificación, seguido
                        de 6 dígitos de la numeración progresiva por
                        aduana.
                """

                numero_pedimento: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "NumeroPedimento",
                        "type": "Attribute",
                        "required": True,
                        "length": 21,
                        "pattern": r"[0-9]{2}  [0-9]{2}  [0-9]{4}  [0-9]{7}",
                    },
                )

            @dataclass
            class CuentaPredial:
                """
                Attributes
                    numero: Atributo requerido para precisar el número
                        de la cuenta predial del inmueble cubierto por
                        el presente concepto, o bien para incorporar los
                        datos de identificación del certificado de
                        participación inmobiliaria no amortizable,
                        tratándose de arrendamiento.
                """

                numero: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Numero",
                        "type": "Attribute",
                        "required": True,
                        "min_length": 1,
                        "max_length": 150,
                        "white_space": "collapse",
                        "pattern": r"[0-9a-zA-Z]{1,150}",
                    },
                )

            @dataclass
            class ComplementoConcepto:
                any_element: List[object] = field(
                    default_factory=list,
                    metadata={
                        "type": "Wildcard",
                        "namespace": "##any",
                    },
                )

            @dataclass
            class Parte:
                """
                Attributes
                    informacion_aduanera: Nodo opcional para introducir
                        la información aduanera aplicable cuando se
                        trate de ventas de primera mano de mercancías
                        importadas o se trate de operaciones de comercio
                        exterior con bienes o servicios.
                    clave_prod_serv: Atributo requerido para expresar la
                        clave del producto o del servicio amparado por
                        la presente parte. Es requerido y deben utilizar
                        las claves del catálogo de productos y
                        servicios, cuando los conceptos que registren
                        por sus actividades correspondan con dichos
                        conceptos.
                    no_identificacion: Atributo opcional para expresar
                        el número de serie, número de parte del bien o
                        identificador del producto o del servicio
                        amparado por la presente parte. Opcionalmente se
                        puede utilizar claves del estándar GTIN.
                    cantidad: Atributo requerido para precisar la
                        cantidad de bienes o servicios del tipo
                        particular definido por la presente parte.
                    unidad: Atributo opcional para precisar la unidad de
                        medida propia de la operación del emisor,
                        aplicable para la cantidad expresada en la
                        parte. La unidad debe corresponder con la
                        descripción de la parte.
                    descripcion: Atributo requerido para precisar la
                        descripción del bien o servicio cubierto por la
                        presente parte.
                    valor_unitario: Atributo opcional para precisar el
                        valor o precio unitario del bien o servicio
                        cubierto por la presente parte. No se permiten
                        valores negativos.
                    importe: Atributo opcional para precisar el importe
                        total de los bienes o servicios de la presente
                        parte. Debe ser equivalente al resultado de
                        multiplicar la cantidad por el valor unitario
                        expresado en la parte. No se permiten valores
                        negativos.
                """

                informacion_aduanera: List[
                    "Comprobante.Conceptos.Concepto.Parte.InformacionAduanera"
                ] = field(
                    default_factory=list,
                    metadata={
                        "name": "InformacionAduanera",
                        "type": "Element",
                    },
                )
                clave_prod_serv: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "ClaveProdServ",
                        "type": "Attribute",
                        "required": True,
                    },
                )
                no_identificacion: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "NoIdentificacion",
                        "type": "Attribute",
                        "min_length": 1,
                        "max_length": 100,
                        "white_space": "collapse",
                        "pattern": r"[^|]{1,100}",
                    },
                )
                cantidad: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "Cantidad",
                        "type": "Attribute",
                        "required": True,
                        "min_inclusive": Decimal("0.000001"),
                        "fraction_digits": 6,
                        "white_space": "collapse",
                    },
                )
                unidad: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Unidad",
                        "type": "Attribute",
                        "min_length": 1,
                        "max_length": 20,
                        "white_space": "collapse",
                        "pattern": r"[^|]{1,20}",
                    },
                )
                descripcion: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Descripcion",
                        "type": "Attribute",
                        "required": True,
                        "min_length": 1,
                        "max_length": 1000,
                        "white_space": "collapse",
                        "pattern": r"[^|]{1,1000}",
                    },
                )
                valor_unitario: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "ValorUnitario",
                        "type": "Attribute",
                        "min_inclusive": "0.000000",
                        "fraction_digits": 6,
                        "white_space": "collapse",
                        "pattern": r"[0-9]{1,18}(.[0-9]{1,6})?",
                    },
                )
                importe: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Importe",
                        "type": "Attribute",
                        "min_inclusive": "0.000000",
                        "fraction_digits": 6,
                        "white_space": "collapse",
                        "pattern": r"[0-9]{1,18}(.[0-9]{1,6})?",
                    },
                )

                @dataclass
                class InformacionAduanera:
                    """
                    Attributes
                        numero_pedimento: Atributo requerido para
                            expresar el número del pedimento que ampara
                            la importación del bien que se expresa en el
                            siguiente formato: últimos 2 dígitos del año
                            de validación seguidos por dos espacios, 2
                            dígitos de la aduana de despacho seguidos
                            por dos espacios, 4 dígitos del número de la
                            patente seguidos por dos espacios, 1 dígito
                            que corresponde al último dígito del año en
                            curso, salvo que se trate de un pedimento
                            consolidado iniciado en el año inmediato
                            anterior o del pedimento original de una
                            rectificación, seguido de 6 dígitos de la
                            numeración progresiva por aduana.
                    """

                    numero_pedimento: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "NumeroPedimento",
                            "type": "Attribute",
                            "required": True,
                            "length": 21,
                            "pattern": r"[0-9]{2}  [0-9]{2}  [0-9]{4}  [0-9]{7}",
                        },
                    )

    @dataclass
    class Impuestos:
        """
        Attributes
            retenciones: Nodo condicional para capturar los impuestos
                retenidos aplicables. Es requerido cuando en los
                conceptos se registre algún impuesto retenido.
            traslados: Nodo condicional para capturar los impuestos
                trasladados aplicables. Es requerido cuando en los
                conceptos se registre un impuesto trasladado.
            total_impuestos_retenidos: Atributo condicional para
                expresar el total de los impuestos retenidos que se
                desprenden de los conceptos expresados en el comprobante
                fiscal digital por Internet. No se permiten valores
                negativos. Es requerido cuando en los conceptos se
                registren impuestos retenidos.
            total_impuestos_trasladados: Atributo condicional para
                expresar el total de los impuestos trasladados que se
                desprenden de los conceptos expresados en el comprobante
                fiscal digital por Internet. No se permiten valores
                negativos. Es requerido cuando en los conceptos se
                registren impuestos trasladados.
        """

        retenciones: Optional["Comprobante.Impuestos.Retenciones"] = field(
            default=None,
            metadata={
                "name": "Retenciones",
                "type": "Element",
            },
        )
        traslados: Optional["Comprobante.Impuestos.Traslados"] = field(
            default=None,
            metadata={
                "name": "Traslados",
                "type": "Element",
            },
        )
        total_impuestos_retenidos: Optional[str] = field(
            default=None,
            metadata={
                "name": "TotalImpuestosRetenidos",
                "type": "Attribute",
                "min_inclusive": "0.000000",
                "fraction_digits": 6,
                "white_space": "collapse",
                "pattern": r"[0-9]{1,18}(.[0-9]{1,6})?",
            },
        )
        total_impuestos_trasladados: Optional[float] = field(
            default=None,
            metadata={
                "name": "TotalImpuestosTrasladados",
                "type": "Attribute",
                "min_inclusive": "0.000000",
                "fraction_digits": 6,
                "white_space": "collapse",
                "pattern": r"[0-9]{1,18}(.[0-9]{1,6})?",
            },
        )

        @dataclass
        class Retenciones:
            """
            Attributes
                retencion: Nodo requerido para la información detallada
                    de una retención de impuesto específico.
            """

            retencion: List["Comprobante.Impuestos.Retenciones.Retencion"] = field(
                default_factory=list,
                metadata={
                    "name": "Retencion",
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class Retencion:
                """
                Attributes
                    impuesto: Atributo requerido para señalar la clave
                        del tipo de impuesto retenido.
                    importe: Atributo requerido para señalar el monto
                        del impuesto retenido. No se permiten valores
                        negativos.
                """

                impuesto: Optional[CImpuesto] = field(
                    default=None,
                    metadata={
                        "name": "Impuesto",
                        "type": "Attribute",
                        "required": True,
                    },
                )
                importe: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Importe",
                        "type": "Attribute",
                        "required": True,
                        "min_inclusive": "0.000000",
                        "fraction_digits": 6,
                        "white_space": "collapse",
                        "pattern": r"[0-9]{1,18}(.[0-9]{1,6})?",
                    },
                )

        @dataclass
        class Traslados:
            """
            Attributes
                traslado: Nodo requerido para la información detallada
                    de un traslado de impuesto específico.
            """

            traslado: List["Comprobante.Impuestos.Traslados.Traslado"] = field(
                default_factory=list,
                metadata={
                    "name": "Traslado",
                    "type": "Element",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class Traslado:
                """
                Attributes
                    base: Atributo requerido para señalar la suma de los
                        atributos Base de los conceptos del impuesto
                        trasladado. No se permiten valores negativos.
                    impuesto: Atributo requerido para señalar la clave
                        del tipo de impuesto trasladado.
                    tipo_factor: Atributo requerido para señalar la
                        clave del tipo de factor que se aplica a la base
                        del impuesto.
                    tasa_ocuota: Atributo condicional para señalar el
                        valor de la tasa o cuota del impuesto que se
                        traslada por los conceptos amparados en el
                        comprobante.
                    importe: Atributo condicional para señalar la suma
                        del importe del impuesto trasladado, agrupado
                        por impuesto, TipoFactor y TasaOCuota. No se
                        permiten valores negativos.
                """

                base: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Base",
                        "type": "Attribute",
                        "required": True,
                        "min_inclusive": "0.000000",
                        "fraction_digits": 6,
                        "white_space": "collapse",
                        "pattern": r"[0-9]{1,18}(.[0-9]{1,6})?",
                    },
                )
                impuesto: Optional[CImpuesto] = field(
                    default=None,
                    metadata={
                        "name": "Impuesto",
                        "type": "Attribute",
                        "required": True,
                    },
                )
                tipo_factor: Optional[CTipoFactor] = field(
                    default=None,
                    metadata={
                        "name": "TipoFactor",
                        "type": "Attribute",
                        "required": True,
                    },
                )
                tasa_ocuota: Optional[Decimal] = field(
                    default=None,
                    metadata={
                        "name": "TasaOCuota",
                        "type": "Attribute",
                        "min_inclusive": Decimal("0.000000"),
                        "fraction_digits": 6,
                        "white_space": "collapse",
                    },
                )
                importe: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Importe",
                        "type": "Attribute",
                        "min_inclusive": "0.000000",
                        "fraction_digits": 6,
                        "white_space": "collapse",
                        "pattern": r"[0-9]{1,18}(.[0-9]{1,6})?",
                    },
                )

    @dataclass
    class Complemento:
        any_element: List[object] = field(
            default_factory=list,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            },
        )

    @dataclass
    class Addenda:
        any_element: List[object] = field(
            default_factory=list,
            metadata={
                "type": "Wildcard",
                "namespace": "##any",
            },
        )
