
* [ ] select_related/prefetch_related
>  If the serializer_class used in the generic view spans orm relations, 
> leading to an n+1 problem, you could optimize your queryset in this method using select_related and prefetch_related.

* [ ] 优化权限: 不传owner修改
* [ ] 排序