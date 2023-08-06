
from .feature_collection import FeatureCollection
from .function_wrapper import FuncWrapper
from .utils import _get_name

class FeatureCollectionTransformer(FeatureCollection):

    def _set_transform_wrapper_fit_flag(self, fit: bool):
        for key in self._feature_desc_dict.keys():
            for wrapped_func in self._feature_desc_dict[key]:
                # wrappedfunc is a FuncWrapper
                if _get_name(wrapped_func.func).startswith("[wrapped_transformer]__"):
                    wrapped_func.kwargs["fit"] = fit    

    def fit(self, data, y=None, **calculate_kwargs):
        self._set_transform_wrapper_fit_flag(fit=True)
        super().calculate(data, **calculate_kwargs)
        self._set_transform_wrapper_fit_flag(fit=False)

    def transform(self, data, y=None, **calculate_kwargs):
        super().calculate(data, **calculate_kwargs)

    def calculate(self, *args, **kwargs):
        raise NotImplementedError("Only .fit and .transform can be called on this object.")


from .utils import _get_funcwrapper_func_and_kwargs
def transformer_wrapper(transformer) -> FuncWrapper:
    from sklearn.base import TransformerMixin
    assert isinstance(transformer, FuncWrapper) or isinstance(transformer, TransformerMixin)
    
    func_wrapper_kwargs = {}
    if isinstance(transformer, FuncWrapper):
        # Extract the function and keyword arguments from the function wrapper
        transformer, func_wrapper_kwargs = _get_funcwrapper_func_and_kwargs(transformer)

    assert isinstance(transformer, TransformerMixin)

    func_wrapper_kwargs["vectorized"] = True
    
    def wrap_transformer(X, fit: bool):
        assert isinstance(fit, bool)
        if not fit:
            return transformer.transform(X)
        return transformer.fit_transform(X)

    wrap_transformer.__name__ = "[wrapped_transformer]__" + transformer.__repr__()
    return FuncWrapper(wrap_transformer, **func_wrapper_kwargs)
