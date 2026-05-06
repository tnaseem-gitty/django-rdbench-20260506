from django.db.migrations.operations.fields import AlterField

class MigrationOptimizer:
    """
    Power the optimization process, where you provide a list of Operations
    and you are returned a list of equal or shorter length - operations
    are merged into one if possible.

    For example, a CreateModel and an AddField can be optimized into a
    new CreateModel, and CreateModel and DeleteModel can be optimized into
    nothing.
    """

    def optimize(self, operations, app_label):
        """
        Main optimization entry point. Pass in a list of Operation instances,
        get out a new list of Operation instances.

        Unfortunately, due to the scope of the optimization (two combinable
        operations might be separated by several hundred others), this can't be
        done as a peephole optimization with checks/output implemented on
        the Operations themselves; instead, the optimizer looks at each
        individual operation and scans forwards in the list to see if there
        are any matches, stopping at boundaries - operations which can't
        be optimized over (RunSQL, operations on the same field/model, etc.)

        The inner loop is run until the starting list is the same as the result
        list, and then the result is returned. This means that operation
        optimization must be stable and always return an equal or shorter list.
        """
        # Internal tracking variable for test assertions about # of loops
        if app_label is None:
            raise TypeError("app_label must be a str.")
        self._iterations = 0
        while True:
            result = self.optimize_inner(operations, app_label)
            self._iterations += 1
            if result == operations:
                return result
            operations = result

    def optimize_inner(self, operations, app_label):
        """
        Inner optimization loop.
        
        This method now optimizes consecutive AlterField operations on the same model and field
        by merging them into a single operation with all the latest field attributes.
        """
        new_operations = []
        i = 0
        while i < len(operations):
            operation = operations[i]
            if isinstance(operation, AlterField):
                # Look ahead for consecutive AlterField operations on the same model and field
                j = i + 1
                while j < len(operations) and isinstance(operations[j], AlterField) and \
                      operations[j].model_name == operation.model_name and \
                      operations[j].name == operation.name:
                    # Merge the field attributes, keeping the latest values
                    new_attrs = operation.field.deconstruct()[3].copy()
                    new_attrs.update(operations[j].field.deconstruct()[3])
                    operation.field = type(operation.field)(**new_attrs)
                    j += 1
                new_operations.append(operation)
                i = j  # Skip the merged operations
            else:
                new_operations.append(operation)
                i += 1

        return new_operations
