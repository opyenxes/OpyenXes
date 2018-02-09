from opyenxes.extension.XExtension import XExtension
from urllib.parse import urlparse
from opyenxes.info.XGlobalAttributeNameMap import XGlobalAttributeNameMap
from opyenxes.factory.XFactoryRegistry import XFactoryRegistry
from opyenxes.utils.SingletonClassGenerator import XSemanticExtensionMetaclass


class XSemanticExtension(XExtension, metaclass=XSemanticExtensionMetaclass):
    """This extension adds semantic attributes to event log objects.
    These semantic attributes reference concepts, which are represented by event
    log objects, as unique URIs.

    Uses the singleton metaclass
    """
    def __init__(self):
        super().__init__("Semantic", "semantic", urlparse("http://www.xes-standard.org/semantic.xesext"))
        factory = XFactoryRegistry().current_default()

        self.ATTR_MODELREFERENCE = factory.create_attribute_literal("semantic:modelReference", "UNKNOWN", self)

        self.get_event_attributes().add(self.ATTR_MODELREFERENCE.clone())
        self.get_trace_attributes().add(self.ATTR_MODELREFERENCE.clone())
        self.get_log_attributes().add(self.ATTR_MODELREFERENCE.clone())
        self.get_meta_attributes().add(self.ATTR_MODELREFERENCE.clone())

        XGlobalAttributeNameMap().register_mapping("EN", "semantic:modelReference", "Ontology Model Reference")
        XGlobalAttributeNameMap().register_mapping("DE", "semantic:modelReference", "Ontologie-Modellreferenz")
        XGlobalAttributeNameMap().register_mapping("FR", "semantic:modelReference", "Référence au Modèle Ontologique")
        XGlobalAttributeNameMap().register_mapping("ES", "semantic:modelReference", "Referencia de Modelo Ontológico")
        XGlobalAttributeNameMap().register_mapping("PT", "semantic:modelReference", "Referência de Modelo Ontológico")

    @staticmethod
    def extract_model_references(target):
        """Retrieves the list of model references which describe a log element
        (archive, log, trace, event, attribute).

        :param target: Any log element (i.e., archive, log, trace, event, or
         attribute) to be queried.
        :type target: XAttributable
        :return: The list of model references, as a list of strings, referred to
         by this element.
        :rtype: list[str]
        """
        model_references = list()
        model_reference_attribute = target.get_attributes().get("semantic:modelReference")
        if model_reference_attribute:
            ref_string = model_reference_attribute.get_value().lower()
            aux = ref_string.split("\\s")
            for i in range(len(aux)):
                reference = aux[i]
                model_references.append(reference.lower())

        return model_references

    def extract_model_reference_uris(self, target):
        """Retrieves the list of model reference URIs which describe a log
        element (archive, log, trace, event, attribute).

        :param target: Any log element (i.e., archive, log, trace, event, or
         attribute) to be queried.
        :type target: `XAttributable`
        :return: The list of model references, as a list of URIs, referred to
         by this element.
        :rtype: list[ParseResult]
        """
        ref_strings = self.extract_model_references(target)
        ref_uri = list()

        for ref_string in ref_strings:
            ref_uri.append(urlparse(ref_string))
        return ref_uri

    def assign_model_references(self, target, model_reference):
        """Assigns to a log element (i.e., archive, log, trace, event, or
         attribute) a list of model references.

        :param target: Any log element (i.e., archive, log, trace, event, or
         attribute) to be assigned references to.
        :type target: `XAttributable`
        :param model_reference: The list of model references, as a list of
         strings, referred to by this element.
        :type model_reference: list[str]
        """
        sb = []
        for ref in model_reference:
            sb.append(ref)
            sb.append(" ")

        aux = "".join(sb)
        if len(aux.lower()) > 0:
            attr = self.ATTR_MODELREFERENCE.clone()
            attr.set_value(aux)
            target.get_attributes()["semantic:modelReference"] = attr

    def assign_model_reference_uris(self, target, model_reference):
        """Assigns to a log element (i.e., archive, log, trace, event, or
         attribute) a list of model references.

        :param target: Any log element (i.e., archive, log, trace, event,
         or attribute) to be assigned references to.
        :type target: `XAttributable`
        :param model_reference: The list of model references, as a list of URIs,
         referred to by this element.
        :type model_reference: list[ParseResult or SplitResult]
        """
        sb = []
        for ref in model_reference:
            sb.append(ref.geturl())
            sb.append(" ")

        aux = "".join(sb)
        if len(aux.lower()) > 0:
            attr = self.ATTR_MODELREFERENCE.clone()
            attr.set_value(aux)
            target.get_attributes()["semantic:modelReference"] = attr
